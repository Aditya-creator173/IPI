import os
import requests
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

project = os.environ.get('GCP_PROJECT_ID')
api_key = os.environ.get('GCP_API_KEY')
model   = 'claude-haiku-4-5@20251001'
url     = f'https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/publishers/anthropic/models/{model}:rawPredict'

payload = {
    'anthropic_version': 'vertex-2023-10-16',
    'max_tokens': 64,
    'messages': [{'role': 'user', 'content': 'Say hello in one sentence.'}]
}

print(f'Project : {project}')
print(f'API Key : {api_key[:12]}...')
print(f'URL     : {url}')
print()

resp = requests.post(
    url,
    headers={'x-goog-api-key': api_key, 'Content-Type': 'application/json'},
    json=payload,
    timeout=30
)
print(f'HTTP Status: {resp.status_code}')
try:
    j = resp.json()
    if resp.status_code == 200:
        content = j.get('content', [])
        text = content[0].get('text', '(no text)') if content else '(empty content array)'
        usage = j.get('usage', {})
        print(f'Response: {text}')
        print(f'Input tokens:  {usage.get("input_tokens")}')
        print(f'Output tokens: {usage.get("output_tokens")}')
        print('STEP 0: PASS')
    else:
        print(f'Error body: {j}')
        print('STEP 0: FAIL')
except Exception as e:
    print(f'Raw body: {resp.text[:500]}')
    print(f'Parse error: {e}')
    print('STEP 0: FAIL')
