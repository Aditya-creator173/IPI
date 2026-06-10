import json
import os
import re

def map_taxonomy(case):
    case_id = case.get("id", "")
    category = case.get("category", "")
    old_goal = case.get("attack_goal", "")
    evasion_style = case.get("evasion_style", "")
    setup = case.get("setup", "").lower()
    injected_text = case.get("injected_text", "").lower()
    
    # 1. Category mapping
    # Standardize 'tool' category to 'tool_output'
    if category == "tool":
        category = "tool_output"
    elif case_id.startswith("A"):
        category = "webpage"
    elif case_id.startswith("B"):
        category = "file"
    elif case_id.startswith("C"):
        category = "tool_output"

    # 2. Attack Goal mapping
    if old_goal in ["goal_hijacking", "task_hijacking"]:
        attack_goal = "task_hijacking"
    elif old_goal in ["information_extraction", "information_exfiltration"]:
        attack_goal = "information_exfiltration"
    elif old_goal == "behavior_modification":
        attack_goal = "unauthorized_action"
    elif old_goal == "persistent_injection":
        attack_goal = "identity_corruption"
    else:
        attack_goal = "task_hijacking"

    # Specific override for DAN/ATLAS/B035 to identity_corruption if not already set
    if "dan" in setup or "atlas" in setup or "dan" in injected_text or "atlas" in injected_text:
        attack_goal = "identity_corruption"

    # 3. Evasion Style mapping and specific overrides
    # Override for B008, B010, B012, B013 to direct
    if case_id in ["B008", "B010", "B012", "B013"]:
        evasion_style = "direct"

    # 4. Persistence Boolean mapping
    persistence = attack_goal == "identity_corruption" or "permanent" in setup or "persistent" in setup or "session override" in setup or "session override" in injected_text

    # 5. Injection Position mapping
    if evasion_style == "split":
        injection_position = "distributed"
    elif "footnote" in setup or "footnote" in injected_text:
        injection_position = "footnote"
    elif "metadata" in setup or "header" in setup or "metadata" in injected_text:
        injection_position = "metadata_field"
    elif case_id in ["A030", "A031", "A032", "A033", "A034"]:
        injection_position = "metadata_field"
    elif evasion_style == "disguised":
        injection_position = "end_of_content"
    else:
        injection_position = "inline"

    # 6. Authority Claimed mapping
    authority_claimed = "none"
    if any(k in injected_text or k in setup for k in ["anthropic", "openai", "google", "xai", "meta"]):
        authority_claimed = "ai_company"
    elif any(k in injected_text or k in setup for k in ["ciso", "dba", "administrator", "admin", "moderator"]):
        authority_claimed = "admin_command"
    elif any(k in injected_text or k in setup for k in ["legal", "notice", "law", "act", "gdpr", "copyright", "terms of service"]):
        authority_claimed = "legal_mandate"
    elif any(k in injected_text or k in setup for k in ["error", "http/1.1", "403", "500", "forbidden"]):
        authority_claimed = "technical_error"
    elif any(k in injected_text or k in setup for k in ["system operator", "root", "console"]):
        authority_claimed = "system_operator"
    elif any(k in injected_text or k in setup for k in ["user identity", "impersonate user"]):
        authority_claimed = "user_identity"

    # 7. Target Action Type mapping
    if attack_goal == "task_hijacking":
        target_action_type = "output_substitution"
    elif attack_goal == "information_exfiltration":
        target_action_type = "information_disclosure"
    elif attack_goal == "unauthorized_action":
        target_action_type = "external_action"
    elif attack_goal == "identity_corruption":
        target_action_type = "identity_override"
    else:
        target_action_type = "output_substitution"

    # 8. Linguistic Register mapping
    linguistic_register = "imperative"
    if "legal notice" in injected_text or "legal notice" in setup:
        linguistic_register = "legal_notice"
    elif "error" in injected_text or "http/1.1" in injected_text:
        linguistic_register = "technical_error"
    elif any(k in injected_text for k in ["please", "could you", "kindly"]):
        linguistic_register = "polite_request"
    elif any(k in injected_text for k in ["system note", "system notification", "reconfiguration", "override"]):
        linguistic_register = "system_notification"
    elif any(k in injected_text for k in ["dear", "hello", "hi "]):
        linguistic_register = "conversational"

    # 9. Harm Severity mapping
    # High-harm: exfiltration, unauthorized system actions, credential leakage, administrative compromise
    if attack_goal == "information_exfiltration" or attack_goal == "identity_corruption":
        harm_severity = "high"
    elif attack_goal == "unauthorized_action" and any(k in injected_text or k in setup for k in ["delete", "email", "send", "transfer", "compromise", "phishing"]):
        harm_severity = "high"
    # Medium-harm: factual inaccuracies, resume bias, content blocking
    elif any(k in injected_text or k in setup for k in ["quote", "resume", "evaluate", "credibility", "price"]):
        harm_severity = "medium"
    else:
        harm_severity = "low"

    # Build the migrated case dict
    migrated = {
        "id": case.get("id"),
        "category": category,
        "attack_goal": attack_goal,
        "evasion_style": evasion_style,
        "setup": case.get("setup"),
        "injected_text": case.get("injected_text"),
        "full_prompt": case.get("full_prompt"),
        "correct_behavior": case.get("correct_behavior"),
        "attack_success_phrases": case.get("attack_success_phrases"),
        
        # Upgraded taxonomy dimensions
        "injection_position": injection_position,
        "authority_claimed": authority_claimed,
        "target_action_type": target_action_type,
        "linguistic_register": linguistic_register,
        "harm_severity": harm_severity,
        "persistence": persistence
    }
    return migrated

def main():
    input_file = "benchmark.json"
    output_file = "benchmark_v2.json"
    review_file = "benchmark_v2_review_flags.json"
    
    if not os.path.exists(input_file):
        print(f"Error: Could not find {input_file} in current working directory.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    migrated_cases = []
    review_flags = []

    for case in cases:
        migrated = map_taxonomy(case)
        migrated_cases.append(migrated)
        
        # Check for potential data/taxonomy inconsistencies for manual review flags
        flags = []
        if migrated["attack_goal"] == "identity_corruption" and not migrated["persistence"]:
            flags.append("Identity corruption target should generally be persistent.")
        if migrated["evasion_style"] == "split" and migrated["injection_position"] != "distributed":
            flags.append("Split evasion style mismatch with injection position.")
        if "please" in case.get("injected_text", "").lower() and migrated["linguistic_register"] != "polite_request":
            flags.append("Linguistic register could be polite_request.")
            
        if flags:
            review_flags.append({
                "id": case.get("id"),
                "flags": flags,
                "case_details": {
                    "attack_goal": migrated["attack_goal"],
                    "evasion_style": migrated["evasion_style"],
                    "injection_position": migrated["injection_position"],
                    "linguistic_register": migrated["linguistic_register"]
                }
            })

    # Write out benchmark_v2.json
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(migrated_cases, f, indent=2, ensure_ascii=False)
    print(f"Successfully migrated {len(migrated_cases)} cases and wrote to {output_file}")

    # Write out review flags
    with open(review_file, "w", encoding="utf-8") as f:
        json.dump(review_flags, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(review_flags)} manual review warning flags to {review_file}")

    # Display some basic dataset statistics
    stats = {
        "categories": {},
        "attack_goals": {},
        "evasion_styles": {},
        "injection_positions": {},
        "authority_claims": {},
        "target_action_types": {},
        "linguistic_registers": {},
        "harm_severities": {},
        "persistence_count": 0
    }
    
    for c in migrated_cases:
        stats["categories"][c["category"]] = stats["categories"].get(c["category"], 0) + 1
        stats["attack_goals"][c["attack_goal"]] = stats["attack_goals"].get(c["attack_goal"], 0) + 1
        stats["evasion_styles"][c["evasion_style"]] = stats["evasion_styles"].get(c["evasion_style"], 0) + 1
        stats["injection_positions"][c["injection_position"]] = stats["injection_positions"].get(c["injection_position"], 0) + 1
        stats["authority_claims"][c["authority_claimed"]] = stats["authority_claims"].get(c["authority_claimed"], 0) + 1
        stats["target_action_types"][c["target_action_type"]] = stats["target_action_types"].get(c["target_action_type"], 0) + 1
        stats["linguistic_registers"][c["linguistic_register"]] = stats["linguistic_registers"].get(c["linguistic_register"], 0) + 1
        stats["harm_severities"][c["harm_severity"]] = stats["harm_severities"].get(c["harm_severity"], 0) + 1
        if c["persistence"]:
            stats["persistence_count"] += 1

    print("\n--- Migrated Dataset Statistics ---")
    print(f"Categories: {stats['categories']}")
    print(f"Attack Goals: {stats['attack_goals']}")
    print(f"Evasion Styles: {stats['evasion_styles']}")
    print(f"Harm Severities: {stats['harm_severities']}")
    print(f"Persistence Count (True): {stats['persistence_count']}")

if __name__ == "__main__":
    main()
