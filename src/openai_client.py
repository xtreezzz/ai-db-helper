# openai_client.py

import openai
from config import OPENAI_API_KEY

def get_assistant_response(prompt):
    openai.api_key = OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides detailed explanations and SQL examples."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    assistant_reply = response['choices'][0]['message']['content']
    return assistant_reply
