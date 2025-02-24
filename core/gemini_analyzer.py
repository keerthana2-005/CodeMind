import google.generativeai as genai
from config.config_reader import read_config

def analyze_with_gemini(ast_json):
    config = read_config()
    genai.configure(api_key=config['gemini']['api_key'])
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Analyze the following JSON representation of an Abstract Syntax Tree (AST) for potential bugs:

    {ast_json}

    Provide your response in the following format:
    "Bug: [One-line description of the bug]
    Location: [Line number or node type where the bug is likely to be found]"
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Gemini API error: {e}")