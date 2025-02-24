from flask import Flask, request, jsonify
from core.ast_analyzer import analyze_ast
from core.code_executor import execute_code
from core.gemini_analyzer import analyze_with_gemini
from core.error_handler import handle_error
import traceback
import os

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_code():
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'error': 'Missing code in request'}), 400

        code = data['code']
        execute_code(code)
        ast_json = analyze_ast(code)
        gemini_response = analyze_with_gemini(ast_json)

        return jsonify({'result': gemini_response})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_file', methods=['POST'])
def analyze_file():
    try:
        data = request.get_json()
        if not data or 'filepath' not in data:
            return jsonify({'error': 'Missing filepath in request'}), 400

        filepath = data['filepath']

        if not os.path.isfile(filepath):
            return jsonify({'error': f"File not found: {filepath}"}), 404

        with open(filepath, 'r') as file:
            code = file.read()

        execute_code(code)
        ast_json = analyze_ast(code)
        gemini_response = analyze_with_gemini(ast_json)

        return jsonify({'result': gemini_response})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) #changed to port 5001