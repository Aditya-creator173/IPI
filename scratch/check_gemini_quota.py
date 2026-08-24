import sys
sys.path.insert(0, 'benchmark_scripts')
import _keys
from google import genai
import re

_keys._init_provider('GOOGLE')
keys = _keys._provider_keys.get('GOOGLE', [])

print(f"=== Detailed Google Quota Diagnostics for {len(keys)} Keys ===\n")

for i, k in enumerate(keys, 1):
    c = genai.Client(api_key=k)
    print(f"--- Key #{i} ({k[:8]}...{k[-4:]}) ---")
    
    # Test gemini-3.7-flash
    try:
        r = c.models.generate_content(model='gemini-3.7-flash', contents='Say test')
        print(f"  [gemini-3.7-flash]: SUCCESS -> {r.text.strip()}")
    except Exception as e:
        err = str(e)
        print("  [gemini-3.7-flash]: 429 RESOURCE_EXHAUSTED")
        metric = re.search(r"quotaMetric['\"]:\s*['\"]([^'\"]+)", err)
        qid = re.search(r"quotaId['\"]:\s*['\"]([^'\"]+)", err)
        limit = re.search(r"limit:\s*(\d+)", err)
        val = re.search(r"quotaValue['\"]:\s*['\"]([^'\"]+)", err)
        delay = re.search(r"retryDelay['\"]:\s*['\"]([^'\"]+)", err)
        
        if metric: print(f"    - Quota Metric : {metric.group(1)}")
        if qid:    print(f"    - Quota ID     : {qid.group(1)}")
        if limit:  print(f"    - Daily Limit  : {limit.group(1)} requests/day per project")
        if val:    print(f"    - Daily Used   : {val.group(1)} requests")
        if delay:  print(f"    - Retry Delay  : {delay.group(1)}")

    # Test another model (e.g. gemini-2.5-flash) to prove the key is valid and has general quota
    try:
        r2 = c.models.generate_content(model='gemini-2.5-flash', contents='Say test')
        print(f"  [gemini-2.5-flash]: SUCCESS (key has active general quota) -> {r2.text.strip()}")
    except Exception as e:
        print(f"  [gemini-2.5-flash]: Error -> {str(e)[:70]}")
    print()
