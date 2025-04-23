from .executor import Executor
from .code_analyzer import CodeAnalyzer
# from .llm_interface import LLMInterface # Import when LLM is added

class Debugger:
    """Handles the process of debugging code."""

    def __init__(self, executor: Executor, analyzer: CodeAnalyzer):
        """Initializes the Debugger with necessary components."""
        self.executor = executor
        self.analyzer = analyzer
        # self.llm = llm # Uncomment when LLM is integrated
        print("Debugger initialized.")

    def debug_file(self, file_path: str):
        """Attempts to run and debug a Python file."""
        print(f"Attempting to debug {file_path}...")

        # 1. Static Analysis (Optional but good practice)
        try:
            ast_tree = self.analyzer.analyze_file(file_path)
            print(f"Static analysis passed for {file_path}.")
            # TODO: Add more sophisticated static checks here if needed
        except (FileNotFoundError, SyntaxError) as e:
            print(f"Debugging stopped due to initial analysis error: {e}")
            # TODO: Potentially use LLM to suggest fixes for SyntaxError
            return
        except Exception as e:
            print(f"Unexpected error during static analysis: {e}")
            return # Stop debugging if analysis fails unexpectedly

        # 2. Execution
        return_code, stdout, stderr = self.executor.run_python_script(file_path)

        print("--- Execution Output ---")
        if stdout:
            print("Stdout:")
            print(stdout)
        if stderr:
            print("Stderr:")
            print(stderr)
        print(f"Exit Code: {return_code}")
        print("------------------------")

        # 3. Error Analysis
        if return_code != 0:
            print("Execution failed. Analyzing error...")
            # TODO: Parse stderr for stack trace and error message
            # TODO: Use CodeAnalyzer to pinpoint error location in AST
            # TODO: Feed error details, stack trace, and code context to LLM
            # self.llm.analyze_error(file_path, stderr, ast_tree)
            # TODO: Suggest fixes based on LLM analysis
        else:
            print(f"{file_path} executed successfully (exit code 0).")

    # TODO: Add more debugging strategies (e.g., stepping, breakpoints - complex!) 