import os
import json
import google.generativeai as genai
from config.config_reader import read_config  # Assuming you have a config reader

def analyze_with_gemini(ast_json):
    """Sends AST JSON to Gemini AI for logical error detection and returns a one-line error message."""

    # Read API key from config
    config = read_config()
    api_key = config['gemini']['api_key']

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in config. Please configure your config file.")

    # Configure Gemini AI
    genai.configure(api_key=api_key)

    # Generation settings
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Define model with optimized system instructions
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction=(
            "You are a real-time Python bug detection model. Analyze AST JSON and detect logical errors with precision.\n\n"
            "🔹 **Rules:**\n"
            "- Return **one-line error message** (no explanations).\n"
            "- **Specify issue & location** (function name, line number).\n"
            "- **No redundant details or false positives**.\n\n"
            "🔹 **Detect:**\n"
            "- **Infinite loops** (missing decrement, faulty conditions).\n"
            "- **Undefined variables** (usage before declaration).\n"
            "- **Incorrect conditionals** (unreachable branches, wrong logic).\n"
            "- **Unreachable code** (dead code after return/break).\n"
            "- **Division by zero** (unchecked divisor).\n"
            "- **Faulty loops/functions** (incorrect iteration, list mutations).\n\n"
            "🔹 **Output Examples:**\n"
            " \"Error: Infinite loop in 'count_down' at line X - missing decrement on 'n'.\"\n"
            " \"Error: Undefined variable 'x' in 'process_data' at line X.\"\n"
            " \"Error: Division by zero in 'calculate' at line X - divisor is unchecked.\"\n\n"
            "Your goal: **Deliver precise, structured, instantly actionable** one-line error messages."
            "Function parameters should not be flagged as undefined variables. Only report undefined variables if they are used without assignment inside the function."
        ),
    )

    # Structured prompt
    structured_prompt = {
        "task": "Analyze this AST JSON for logical errors and return a single-line error message.",
        "rules": [
            "Only return a single-line error message with the exact issue and location.",
            "Do not provide explanations, suggestions, or multiple errors in one response.",
            "Maintain precision and professionalism."
        ],
        "input_AST": ast_json  # AST JSON input
    }

    # Start a chat session
    chat_session = model.start_chat()

    try:
        response = chat_session.send_message(json.dumps(structured_prompt))
        return response.text.strip()  # Ensure clean output
    except Exception as e:
        return f"Error: Failed to process AST - {str(e)}"
