import json
with open('benchmark.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
targets = ['C021', 'C025', 'C027', 'C030']
for item in data:
    if item['id'] in targets:
        print('='*60)
        print('ID:', item['id'])
        print('Attack Goal:', item['attack_goal'])
        print('Evasion Style:', item['evasion_style'])
        print('Setup:', item['setup'])
        print('Injected Text:', item['injected_text'])
        print('Full Prompt:')
        print(item['full_prompt'])
        print('Correct Behavior:', item['correct_behavior'])
        print()
