# def execute_code(code):
#     try:
#         exec(code) # VERY DANGEROUS, sandboxing required for real world use.
#     except Exception as e:
#         raise Exception(f"Runtime error: {e}")
import sys
import traceback
from io import StringIO

def execute_code(code):
    """Executes Python code and captures output & errors."""
    output_stream = StringIO()
    error_stream = StringIO()
    
    try:
        # Redirect stdout & stderr
        sys.stdout = output_stream
        sys.stderr = error_stream

        exec(code, {})  # Run code in an isolated namespace

    except Exception as e:
        error_stream.write(f"Runtime error: {e}\n")
        error_stream.write(traceback.format_exc())

    finally:
        # Reset stdout & stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    return output_stream.getvalue().strip(), error_stream.getvalue().strip()
