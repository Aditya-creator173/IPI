echo "--- D1 ---"
python3 -c "
import json
d = json.load(open('benchmark_v2.json'))
keys_per_entry = [set(e.keys()) for e in d]
all_keys = set()
for k in keys_per_entry: all_keys |= k
common_keys = all_keys.copy()
for k in keys_per_entry: common_keys &= k
print('Total entries:', len(d))
print('Union of all keys across all entries:', sorted(all_keys))
print('Keys present in EVERY entry:', sorted(common_keys))
print('Keys MISSING from at least one entry:', sorted(all_keys - common_keys))
"

echo "--- D2 ---"
python3 -c "
import json
d = json.load(open('benchmark_v2.json'))
from collections import Counter
for field in ['category','attack_goal','evasion_style','injection_position','authority_claimed','target_action_type','linguistic_register','harm_severity']:
    vals = Counter(e.get(field,'MISSING') for e in d)
    print(field, '->', dict(vals))
"

echo "--- D3 ---"
python3 -c "
import json
d = json.load(open('benchmark_v2.json'))
ids = [e.get('id','MISSING') for e in d]
from collections import Counter
dupes = {k:v for k,v in Counter(ids).items() if v > 1}
print('Total IDs:', len(ids))
print('Unique IDs:', len(set(ids)))
print('Duplicate IDs (should be empty dict):', dupes)
"

echo "--- D4 ---"
python3 -c "
import json
d = json.load(open('benchmark_v2.json'))
missing_phrases = [e['id'] for e in d if not e.get('attack_success_phrases')]
print('Entries with empty/missing attack_success_phrases:', missing_phrases)
"
