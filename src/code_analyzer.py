import ast

class CodeAnalyzer:
    """Analyzes Python source code."""

    def __init__(self):
        pass

    def analyze_file(self, file_path: str) -> ast.AST:
        """Reads a Python file and returns its Abstract Syntax Tree (AST)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            return ast.parse(code)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            raise
        except SyntaxError as e:
            print(f"Error: Syntax error in {file_path}: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while analyzing {file_path}: {e}")
            raise

    # TODO: Add methods for more specific analysis
    # e.g., find_function_definitions, check_complexity, etc. 