def execute_code(code):
    try:
        exec(code) # VERY DANGEROUS, sandboxing required for real world use.
    except Exception as e:
        raise Exception(f"Runtime error: {e}")