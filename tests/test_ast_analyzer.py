import unittest
import json
import ast
from core.ast_analyzer import analyze_ast  # Update this import to match your module structure

class TestASTAnalysis(unittest.TestCase):

    def parse_ast_output(self, result):
        """Helper function to parse AST output and handle errors gracefully."""
        try:
            ast_data = json.loads(result)
            if "error" in ast_data:
                self.fail(f"AST returned an error: {ast_data['error']}")
            return ast_data
        except json.JSONDecodeError:
            self.fail("AST output is not valid JSON")

    def test_simple_function(self):
        code = """
def greet():
    print("Hello, World!")
        """
        result = analyze_ast(code)
        ast_data = self.parse_ast_output(result)

        self.assertIsInstance(ast_data, list)
        self.assertEqual(ast_data[0]['type'], "Module")
        self.assertEqual(ast_data[0]['body'][0]['type'], "FunctionDef")
        self.assertEqual(ast_data[0]['body'][0]['name'], "greet")

    def test_syntax_error(self):
        code = """
def test_func(
    print("Invalid syntax")
        """  # Missing closing parenthesis
        result = analyze_ast(code)
        ast_data = json.loads(result)  # No need to use parse_ast_output since error is expected
        
        self.assertIn("error", ast_data)
        self.assertIn("Syntax error", ast_data["error"])  # ✅ Expecting a syntax error

    def test_while_loop(self):
        code = """
def count_down(n):
    while n > 0:
        print(n)
        n -= 1
        """
        result = analyze_ast(code)
        ast_data = self.parse_ast_output(result)

        self.assertEqual(ast_data[0]['body'][0]['type'], "FunctionDef")
        self.assertEqual(ast_data[0]['body'][0]['name'], "count_down")
        
        while_node = ast_data[0]['body'][0]['body'][0]
        self.assertEqual(while_node['type'], "While")
        self.assertEqual(while_node['test']['type'], "Compare")

    def test_logical_error(self):
        code = """
def find_max(lst):
    max_val = 0  # Logical Error: Should use lst[0]
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val
        """
        result = analyze_ast(code)
        ast_data = self.parse_ast_output(result)

        self.assertEqual(ast_data[0]['body'][0]['type'], "FunctionDef")
        self.assertEqual(ast_data[0]['body'][0]['name'], "find_max")
        
        assign_node = ast_data[0]['body'][0]['body'][0]
        self.assertEqual(assign_node['type'], "Assign")
        self.assertEqual(assign_node['targets'][0]['id'], "max_val")

if __name__ == "__main__":
    unittest.main()
