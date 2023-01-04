import openai
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import admin
from dotenv import load_dotenv
import requests
from .models import Host, CVE
load_dotenv('.env')

openai.api_key = os.getenv('OPEN-AI-API-KEY')
api_endpoint = "https://api.openai.com/v1/completions"

def getCVEFix(cve):
    prompt = (f'Can you explain how to fix {cve}')
    payload = {":"}
    payload = {
    "model": "text-davinci-003",
    "prompt": f"How do I fix the {cve} vulnerabilities?",
    "max_tokens": 100,
    "temperature": 0.5,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
    }

# Make the request
    response = requests.post(api_endpoint, json=payload, headers={"Authorization": f"Bearer {openai.api_key}"})

    # Get the completed text from the response
    completed_text = response.json()["choices"][0]["text"]
    return(completed_text)
    