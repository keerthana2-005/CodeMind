import sys
import os
import unittest
from unittest.mock import patch

# Add the core directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core")))

# Import the function from gemini_analyzer
from gemini_analyzer import analyze_with_gemini


class TestGeminiAnalyzer(unittest.TestCase):

    @patch("gemini_analyzer.genai.GenerativeModel")
    def test_empty_ast_json(self, mock_model):
        """Test how function handles an empty AST JSON."""
        mock_model.return_value.start_chat.return_value.send_message.return_value.text = ""
        response = analyze_with_gemini({})
        self.assertEqual(response, "")

    @patch("gemini_analyzer.read_config")
    def test_missing_api_key(self, mock_read_config):
        """Test if function raises an error when API key is missing."""
        mock_read_config.return_value = {"gemini": {"api_key": None}}
        with self.assertRaises(ValueError) as context:
            analyze_with_gemini({"ast": "sample"})
        self.assertIn("GEMINI_API_KEY is not set", str(context.exception))

    @patch("gemini_analyzer.genai.GenerativeModel")
    def test_unexpected_api_error(self, mock_model):
        """Test if function handles unexpected errors from Gemini API."""
        mock_model.return_value.start_chat.return_value.send_message.side_effect = Exception("API Error")
        response = analyze_with_gemini({"ast": "sample"})
        self.assertTrue(response.startswith("Error: Failed to process AST"))

    @patch("gemini_analyzer.genai.GenerativeModel")
    def test_valid_ast_input(self, mock_model):
        """Test if analyze_with_gemini processes a valid AST JSON correctly."""
        mock_model.return_value.start_chat.return_value.send_message.return_value.text = "Error: Undefined variable 'x' in function 'foo' at line 3."
        response = analyze_with_gemini({"ast": "valid_ast"})
        self.assertEqual(response, "Error: Undefined variable 'x' in function 'foo' at line 3.")


if __name__ == "__main__":
    unittest.main()
