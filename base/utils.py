# utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(user_email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )



import requests

OPENAI_API_KEY = 'your_api_key_here'  # Replace with your API key

def chat_gpt(prompt):
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"  # API endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "prompt": prompt,  # User input prompt
        "max_tokens": 150  # Limit on how much the response can generate
    }
    response = requests.post(url, headers=headers, json=data)  # Send the request
    return response.json()['choices'][0]['text'] if response.status_code == 200 else None  # Handle responsez