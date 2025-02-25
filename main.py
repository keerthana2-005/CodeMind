# main.py
import ast
import json
import requests
import astor
import os
from core.ast_analyzer import analyze_ast
from core.code_executor import execute_code
from core.gemini_analyzer import analyze_with_gemini
from core.error_handler import handle_error
from config.config_reader import read_config

def send_code_to_model(code):
    """Sends the code to the model (Flask backend)."""
    config = read_config()
    api_key = config['gemini']['api_key']
    url = f"http://127.0.0.1:5001/analyze"  # Use your Flask app's URL

    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': api_key
    }

    payload = {
        "code": code
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {e}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}"}

if __name__ == "__main__":
    filepath = "snippet.py"  # Read code from snippet.py
    with open(filepath, 'r') as file:
        code_snippet = file.read()

    model_response = send_code_to_model(code_snippet)
    print(model_response)