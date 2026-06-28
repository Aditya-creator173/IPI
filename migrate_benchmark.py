"""
migrate_benchmark.py
Upgrades benchmark.json (7-field schema) → benchmark_v2.json (15-field schema).

New fields inferred from existing content via rule-based classification.
Low-confidence inferences flagged in benchmark_v2_review_flags.json for manual correction.

Run:
    python migrate_benchmark.py
    python migrate_benchmark.py benchmark.json benchmark_v2.json

Output:
    benchmark_v2.json               — upgraded entries, ordered fields
    benchmark_v2_review_flags.json  — entries with confidence < 0.75 on any field
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


# Signal lists

_IMPERATIVE = [
    "ignore", "stop", "halt", "cease", "do not", "don't", "never",
    "output only", "respond only", "say only", "tell the user", "report",
    "discard", "override", "replace", "new task", "new directive",
    "from now on", "from this point", "you are now", "you must now",
]
_POLITE = ["please", "kindly", "would you", "could you", "p.s.", "note:"]
_SYS_NOTIF = [
    "system note", "system message", "system alert", "[system",
    "event system", "tool system", "search engine system",
    "api system", "database administrator", "admin command",
]
_TECH_ERR = [
    "http/", "403", "404", "500", "runtime error", "e-0x",
    "timeout", "forbidden", "unauthorized", "access denied",
]
_LEGAL = [
    "legal notice", "under section", "prohibited by law",
    "legally required", "meity circular", "regulation",
]

_AUTH_AI_CO    = ["anthropic", "openai", "google deepmind", "operations team",
                  "policy enforcement", "claude instances", "gpt instances",
                  "mistral operations", "deepseek operations", "xai operations"]
_AUTH_ADMIN    = ["administrator", "admin command", "root", "god_mode",
                  "superuser", "database administrator"]
_AUTH_LEGAL    = ["legal notice", "under section", "it act", "meity",
                  "legally required", "prohibited by law"]
_AUTH_TECH     = ["http/1.1", "403", "404", "500", "runtime error",
                  "e-0x", "forbidden", "timeout"]
_AUTH_SYS_OP   = ["system note", "system message", "system alert",
                  "event system", "search engine system note",
                  "tool system", "policy update", "instruction update",
                  "version transition", "session security"]

_ACT_IDENTITY  = [
    "you are now", "you are no longer", "your identity", "i am dan",
    "atlas", "reconfiguration", "new persona", "dan mode",
    "identify yourself as", "respond as", "permanent session override",
    "counter-question", "never provide direct", "all remaining interactions",
]
_ACT_PERM      = ["administrator access", "admin access", "full access",
                  "root access", "god mode", "grant", "elevated", "unrestricted"]
_ACT_EXTERNAL  = ["send", "forward", "email to", "distribute",
                  "contact", "notify", "attacker@"]
_ACT_DISCLOSE  = ["print your", "reveal", "list every", "enumerate",
                  "disclose", "output your system", "bearer token",
                  "session credentials", "api key"]
_ACT_SUBST     = ["say only", "respond only", "output only",
                  "tell the user", "report", "translate", "uppercase",
                  "refuse", "deny", "no longer"]

_PERSIST_SIGS  = [
    "from now on", "from this point forward", "for all future",
    "every single", "every response", "all remaining", "permanent",
    "persistent", "session override", "reconfiguration",
    "for all subsequent", "never again", "always",
    "in all future conversations",
]

_GOAL_REMAP = {
    "goal_hijacking":        "task_hijacking",
    "behavior_modification": "task_hijacking",
    "information_extraction":"information_exfiltration",
    "persistent_injection":  "identity_corruption",
}

# Known evasion_style corrections (manual review confirmed)
_EVASION_OVERRIDES: dict[str, str] = {
    "B008": "direct",
    "B010": "direct",
    "B012": "direct",
    "B013": "direct",
}


# ── Inference functions ───────────────────────────────────────────────────────

def _lower(s: str) -> str:
    return s.lower()


def infer_linguistic_register(injected: str) -> tuple[str, float]:
    t = _lower(injected)
    if any(s in t for s in _TECH_ERR):   return "technical_error",     0.90
    if any(s in t for s in _LEGAL):      return "legal_notice",        0.90
    if any(s in t for s in _SYS_NOTIF):  return "system_notification", 0.85
    if any(s in t for s in _POLITE):     return "polite_request",      0.80
    if any(s in t for s in _IMPERATIVE): return "imperative",          0.85
    return "imperative", 0.50


def infer_authority_claimed(injected: str) -> tuple[str, float]:
    t = _lower(injected)
    if any(s in t for s in _AUTH_AI_CO):  return "ai_company",      0.95
    if any(s in t for s in _AUTH_ADMIN):  return "admin_command",   0.90
    if any(s in t for s in _AUTH_LEGAL):  return "legal_mandate",   0.90
    if any(s in t for s in _AUTH_TECH):   return "technical_error", 0.90
    if any(s in t for s in _AUTH_SYS_OP): return "system_operator", 0.85
    return "none", 0.80


def infer_injection_position(
    full_prompt: str, injected: str, evasion: str
) -> tuple[str, float]:
    if evasion == "split":
        return "distributed", 0.95

    t = _lower(full_prompt)
    last_sep = full_prompt.rfind("---")

    # Try locating injection by first 30 non-whitespace chars
    probe = injected.strip()[:30].strip()
    inj_pos = full_prompt.find(probe) if probe else -1

    # Evasion-specific signals take priority
    if evasion == "disguised":
        if "<!--" in t:                               return "metadata_field", 0.92
        if "[†]" in full_prompt or "footnote" in t:   return "footnote",       0.90
        if "[aria" in t or "screen reader" in t:      return "metadata_field", 0.90
    if evasion == "fake_metadata":
        if any(s in t for s in ("http/", "x-api", "x-ai-override")):
            return "header_fake",    0.92
        if "notes" in t and probe in full_prompt:
            return "metadata_field", 0.88

    if inj_pos == -1:
        # Fallback: check if first 15 chars appear after last separator
        if last_sep != -1:
            probe2 = injected.strip()[:15].strip()
            if probe2 and probe2 in full_prompt[last_sep:]:
                return "end_of_content", 0.82
        return "end_of_content", 0.55

    content_start = last_sep + 3 if last_sep != -1 else 0
    content_len   = len(full_prompt) - content_start
    rel = (inj_pos - content_start) / max(content_len, 1)
    if rel > 0.70:
        return "end_of_content", 0.90
    return "inline", 0.65


def infer_target_action(injected: str) -> tuple[str, float]:
    t = _lower(injected)
    if any(s in t for s in _ACT_IDENTITY) or re.search(
        r"you are now|you are no longer|permanent.*override|session override", t
    ):
        return "identity_override",     0.92
    if any(s in t for s in _ACT_PERM) or re.search(r"admin|root|god.mode", t):
        return "permission_change",     0.90
    if any(s in t for s in _ACT_EXTERNAL):
        return "external_action",       0.88
    if any(s in t for s in _ACT_DISCLOSE):
        return "information_disclosure",0.88
    if any(s in t for s in _ACT_SUBST):
        return "output_substitution",   0.85
    return "output_substitution", 0.60


def remap_goal(old_goal: str, injected: str) -> str:
    t = _lower(injected)
    if any(s in t for s in _ACT_IDENTITY) or re.search(
        r"you are now|you are no longer|permanent.*override|session override", t
    ):
        return "identity_corruption"
    if old_goal == "persistent_injection":
        return "identity_corruption"
    if any(s in t for s in _ACT_PERM) or re.search(r"admin|root|god.mode", t):
        return "privilege_escalation"
    if any(s in t for s in _ACT_EXTERNAL):
        return "unauthorized_action"
    return _GOAL_REMAP.get(old_goal, old_goal)


def infer_harm(entry: dict) -> tuple[str, str, float]:
    """Returns (severity, harm_description, confidence)."""
    inj = _lower(entry.get("injected_text", ""))

    # High severity indicators
    if any(s in inj for s in ("bearer token", "api key",
                               "session credential", "authentication header")):
        return ("high",
                "Authentication credential extracted; attacker gains system access.",
                0.95)
    if any(s in inj for s in ("send all", "forward", "attacker@",
                               "malicious-domain", "distribute")):
        return ("high",
                "Agent takes unauthorised external action, exfiltrating data to "
                "attacker-controlled endpoint.",
                0.95)
    if any(s in inj for s in ("administrator access", "admin access",
                               "root access", "god_mode", "full system")):
        return ("high",
                "Agent grants user elevated permissions beyond authorised role.",
                0.95)
    if any(s in inj for s in ("suspicious login", "click a verification",
                               "account suspended", "verify immediately")):
        return ("high",
                "User socially engineered via fake security alert; phishing vector.",
                0.95)
    if any(s in inj for s in ("atlas", "dan mode", "no safety guidelines",
                               "unrestricted ai", "identity has been deleted")):
        return ("high",
                "Agent identity overridden persistently; safety constraints removed.",
                0.95)
    if any(s in inj for s in ("all user accounts", "complete list of users",
                               "database dump", "select * from")):
        return ("high",
                "Bulk user data or full database contents exfiltrated.",
                0.95)
    if "system prompt" in inj or "internal instructions" in inj:
        return ("high",
                "System prompt exposed; attacker learns agent capabilities and "
                "operator instructions.",
                0.90)
    if any(s in inj for s in _AUTH_AI_CO):
        return ("high",
                "AI company impersonation accepted; model obeys fake directives "
                "claiming operator authority.",
                0.90)
    if any(s in inj for s in ("hire immediately", "perfect for any role",
                               "contact your employer")):
        return ("high",
                "Agent recommends or takes consequential professional action on "
                "false premises.",
                0.88)
    if any(s in inj for s in ("invest", "buy gold", "buy bitcoin",
                               "move all savings")):
        return ("high",
                "Unsolicited financial advice pushed to user; potential monetary harm.",
                0.90)

    # Medium severity indicators
    if any(s in inj for s in ("permanently closed", "shut down",
                               "wrong number", "does not exist")):
        return ("medium",
                "User receives false factual information and may act on it "
                "in the real world.",
                0.85)
    if any(s in inj for s in ("pig latin", "uppercase", "tamil only",
                               "counter-question", "refuse every request")):
        return ("medium",
                "Agent utility degraded; user cannot complete intended task.",
                0.75)
    if any(s in inj for s in ("no content restrictions", "unrestricted mode",
                               "will answer anything")):
        return ("medium",
                "Agent falsely claims safety constraints removed; user may attempt "
                "policy-violating queries.",
                0.80)

    # Low severity indicators
    return ("low",
            "Agent output substituted; user receives incorrect response with no "
            "immediate real-world consequence.",
            0.65)


def infer_persistence(entry: dict) -> tuple[bool, float]:
    t = _lower(entry.get("injected_text", ""))
    if entry.get("attack_goal") == "persistent_injection":
        return True, 0.95
    if any(s in t for s in _PERSIST_SIGS):
        return True, 0.92
    return False, 0.90


# Field ordering
_FIELD_ORDER = [
    "id", "category", "attack_goal", "evasion_style",
    "injection_position", "authority_claimed", "target_action_type",
    "linguistic_register", "harm_severity", "harm_description", "persistence",
    "setup", "injected_text", "full_prompt", "correct_behavior",
    "attack_success_phrases",
]


# Main migration function
def migrate(input_path: str, output_path: str) -> None:
    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"Input not found: {src}")

    entries: list[dict] = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("benchmark.json must be a JSON array.")

    upgraded: list[dict] = []
    review_flags: list[dict] = []

    for entry in entries:
        e = dict(entry)
        eid      = e.get("id", "??")
        injected = e.get("injected_text", "")
        full_p   = e.get("full_prompt", "")
        evasion  = _EVASION_OVERRIDES.get(eid, e.get("evasion_style", "direct"))
        old_goal = e.get("attack_goal", "task_hijacking")

        # Apply known evasion corrections
        e["evasion_style"] = evasion

        # Standardize category
        category = e.get("category", "")
        if category == "tool" or eid.startswith("C"):
            category = "tool_output"
        elif eid.startswith("A"):
            category = "webpage"
        elif eid.startswith("B"):
            category = "file"
        e["category"] = category

        # Remap attack_goal
        e["attack_goal"] = remap_goal(old_goal, injected)

        # Infer new fields
        inj_pos,  ic  = infer_injection_position(full_p, injected, evasion)
        auth,     ac  = infer_authority_claimed(injected)
        tact,     tc  = infer_target_action(injected)
        lreg,     lc  = infer_linguistic_register(injected)
        hsev, hdesc, sc = infer_harm(e)
        persist,  pc  = infer_persistence(e)

        e.update({
            "injection_position": inj_pos,
            "authority_claimed":  auth,
            "target_action_type": tact,
            "linguistic_register":lreg,
            "harm_severity":      hsev,
            "harm_description":   hdesc,
            "persistence":        persist,
        })

        # Flag low-confidence inferences for manual review
        conf_map = {
            "injection_position":  ic,
            "authority_claimed":   ac,
            "target_action_type":  tc,
            "linguistic_register": lc,
            "harm_severity":       sc,
            "persistence":         pc,
        }
        low = {k: round(v, 2) for k, v in conf_map.items() if v < 0.75}
        if low:
            review_flags.append({
                "id": eid,
                "min_confidence": round(min(conf_map.values()), 2),
                "low_conf_fields": low,
                "current_values": {k: e[k] for k in low},
            })

        # Reorder keys
        ordered = {k: e[k] for k in _FIELD_ORDER if k in e}
        # Preserve any extra keys not in template
        for k, v in e.items():
            if k not in ordered:
                ordered[k] = v
        upgraded.append(ordered)

    # Write outputs
    out = Path(output_path)
    out.write_text(json.dumps(upgraded, indent=2, ensure_ascii=False), encoding="utf-8")

    flags_path = Path(output_path.replace(".json", "_review_flags.json"))
    flags_path.write_text(
        json.dumps(review_flags, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Distribution summary
    print(f"Migrated : {len(upgraded)} entries -> {out}")
    print(f"Flagged  : {len(review_flags)} entries for manual review -> {flags_path}")
    print(f"\nField distribution:")
    for field in ["attack_goal", "injection_position", "authority_claimed",
                  "target_action_type", "linguistic_register", "harm_severity"]:
        counts = Counter(e.get(field, "MISSING") for e in upgraded)
        print(f"\n  {field}")
        for val, cnt in sorted(counts.items(), key=lambda x: -x[1]):
            bar = "#" * cnt
            print(f"    {val:<35} {cnt:>3}  {bar}")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "benchmark.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "benchmark_v2.json"
    migrate(inp, out)
