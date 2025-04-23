import sys
import json
import os
from .executor import Executor
# from .llm_interface import LLMInterface # Import when LLM is added

class TestRunner:
    """Handles running unit tests (e.g., using pytest) and parsing results."""

    def __init__(self, executor: Executor):
        """Initializes the TestRunner with an Executor."""
        self.executor = executor
        # self.llm = llm # Uncomment when LLM is integrated
        print("TestRunner initialized.")

    def run_pytest(self, target: str = ".", cwd: str = None) -> dict:
        """Runs pytest on a given target directory or file and parses JSON report.

        Args:
            target: The file or directory to run tests on (defaults to current dir).
            cwd: The working directory to run pytest from.

        Returns:
            A dictionary containing the parsed test results or an error message.
        """
        report_file = "pytest_report.json"
        # Command to run pytest and generate a JSON report
        # --disable-warnings: Optional, to reduce noise in stdout/stderr
        # -qq: Quieter output to focus on the report file
        command = [
            sys.executable, "-m", "pytest", target,
            f"--json-report-file={report_file}",
            "--disable-warnings", "-qq"
        ]

        print(f"Running pytest on target: '{target}'...")
        return_code, stdout, stderr = self.executor.run_command(command, cwd=cwd)

        if stdout:
            print("Pytest Stdout:")
            print(stdout)
        if stderr:
            print("Pytest Stderr:")
            print(stderr)

        # Try to read and parse the JSON report regardless of exit code,
        # as it might contain partial results even if some tests failed.
        try:
            # Construct the full path to the report file if cwd was used
            report_path = os.path.join(cwd, report_file) if cwd else report_file
            with open(report_path, 'r') as f:
                results = json.load(f)
            print(f"Successfully parsed test report: {report_path}")
            # TODO: Optionally remove the report file after parsing
            # os.remove(report_path)
            return results
        except FileNotFoundError:
            print(f"Error: Pytest JSON report file not found ({report_file}). Pytest exit code: {return_code}")
            # TODO: Use LLM to analyze stdout/stderr if report is missing
            return {"error": "JSON report not found", "exit_code": return_code, "stdout": stdout, "stderr": stderr}
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse pytest JSON report ({report_file}): {e}")
            return {"error": "Failed to parse JSON report", "details": str(e), "exit_code": return_code}
        except Exception as e:
            print(f"An unexpected error occurred while handling test results: {e}")
            return {"error": "Unexpected error handling report", "details": str(e)}

    # TODO: Add method to analyze test failures (using LLM?)
    # def analyze_failures(self, test_results: dict):
    #     pass

    # TODO: Add method to generate test cases (using LLM?)
    # def generate_tests(self, file_path: str):
    #     pass 