#!/usr/bin/env python3
from llm import call_llm_model

print('Testing LLM function...')
messages = [{'role': 'user', 'content': 'Hello, this is a test.'}]

try:
    response = call_llm_model('openai/gpt-4.1-mini', messages)
    print('LLM call successful!')
    print('Response length:', len(response))
    print('Response preview:', response[:100] + '...' if len(response) > 100 else response)
except Exception as e:
    print('Error:', e)