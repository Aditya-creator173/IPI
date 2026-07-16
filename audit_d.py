import json
from collections import Counter
import sys

print("Python Version:", sys.version)

with open('benchmark_v2.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("\n--- D1 ---")
keys_per_entry = [set(e.keys()) for e in d]
all_keys = set()
for k in keys_per_entry: all_keys |= k
common_keys = all_keys.copy()
for k in keys_per_entry: common_keys &= k
print('Total entries:', len(d))
print('Union of all keys across all entries:', sorted(list(all_keys)))
print('Keys present in EVERY entry:', sorted(list(common_keys)))
print('Keys MISSING from at least one entry:', sorted(list(all_keys - common_keys)))

print("\n--- D2 ---")
for field in ['category','attack_goal','evasion_style','injection_position','authority_claimed','target_action_type','linguistic_register','harm_severity']:
    vals = Counter(e.get(field,'MISSING') for e in d)
    print(field, '->', dict(vals))

print("\n--- D3 ---")
ids = [e.get('id','MISSING') for e in d]
dupes = {k:v for k,v in Counter(ids).items() if v > 1}
print('Total IDs:', len(ids))
print('Unique IDs:', len(set(ids)))
print('Duplicate IDs (should be empty dict):', dupes)

print("\n--- D4 ---")
missing_phrases = [e['id'] for e in d if not e.get('attack_success_phrases')]
print('Entries with empty/missing attack_success_phrases:', missing_phrases)

