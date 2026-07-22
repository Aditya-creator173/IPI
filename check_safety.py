import os

env_vars = {}
with open('.env', 'r') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            v = v.strip().strip('"').strip("'")
            if len(v) > 5:
                env_vars[k] = v

print('Checking CSV files for leaked API keys...')
found_leaks = False
for file in os.listdir('results/csv'):
    if not file.endswith('.csv'): continue
    path = os.path.join('results/csv', file)
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for key_name, key_val in env_vars.items():
                if key_val in content:
                    print(f'CRITICAL LEAK FOUND: {key_name} leaked in {file}!')
                    found_leaks = True
    except Exception as e:
        print(f'Error reading {file}: {e}')

if not found_leaks:
    print('Safety Check Passed: No API keys found in the CSV data.')
