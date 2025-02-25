import unittest
import sys
import os

# Add project root to sys.path to fix module import issue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core")))

from code_executor import execute_code  # Now it should import correctly!

class TestCodeExecuter(unittest.TestCase):

    def test_valid_code(self):
        """Test execution of valid Python code."""
        code = "print('Hello, World!')"
        output, error = execute_code(code)
        self.assertEqual(output, "Hello, World!")
        self.assertEqual(error, "")

    def test_syntax_error(self):
        """Test syntax errors."""
        code = "print('Hello"  # Missing closing quote
        output, error = execute_code(code)
        self.assertEqual(output, "")
        self.assertIn("SyntaxError", error)

    def test_runtime_error(self):
        """Test runtime errors like division by zero."""
        code = "x = 1 / 0"
        output, error = execute_code(code)
        self.assertEqual(output, "")
        self.assertIn("ZeroDivisionError", error)

    def test_variable_scope(self):
        """Test that variables from one execution do not persist."""
        execute_code("x = 42")  # Run first
        output, error = execute_code("print(x)")  # Try to access 'x'
        self.assertIn("NameError", error)  # Should not persist

if __name__ == "__main__":
    unittest.main()
