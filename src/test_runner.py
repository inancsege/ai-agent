import sys
import json
import os
import tempfile
from typing import Dict, List, Optional, Union
from pathlib import Path
from .executor import Executor
from .llm_interface import LLMInterface
from .code_analyzer import CodeAnalyzer

class TestRunner:
    """Handles running unit tests (e.g., using pytest) and parsing results."""

    def __init__(self, executor: Executor, llm: Optional[LLMInterface] = None, 
                 code_analyzer: Optional[CodeAnalyzer] = None):
        """Initializes the TestRunner with an Executor and optional LLM interface.
        
        Args:
            executor: The Executor instance for running commands
            llm: Optional LLMInterface for AI-powered analysis and test generation
            code_analyzer: Optional CodeAnalyzer for code analysis
        """
        self.executor = executor
        self.llm = llm
        self.code_analyzer = code_analyzer
        self.temp_dir = tempfile.TemporaryDirectory()
        print("TestRunner initialized.")

    def run_pytest(self, target: str = ".", cwd: str = None, 
                  pytest_args: Optional[List[str]] = None) -> dict:
        """Runs pytest on a given target directory or file and parses JSON report.

        Args:
            target: The file or directory to run tests on (defaults to current dir)
            cwd: The working directory to run pytest from
            pytest_args: Additional pytest arguments (e.g., ['-v', '-m', 'not slow'])

        Returns:
            A dictionary containing the parsed test results or an error message
        """
        # Create a unique report file in the temp directory
        report_file = os.path.join(self.temp_dir.name, f"pytest_report_{os.getpid()}.json")
        
        # Base pytest command
        command = [
            sys.executable, "-m", "pytest", target,
            f"--json-report-file={report_file}",
            "--disable-warnings", "-qq"
        ]
        
        # Add any additional pytest arguments
        if pytest_args:
            command.extend(pytest_args)

        print(f"Running pytest on target: '{target}'...")
        return_code, stdout, stderr = self.executor.run_command(command, cwd=cwd)

        if stdout:
            print("Pytest Stdout:")
            print(stdout)
        if stderr:
            print("Pytest Stderr:")
            print(stderr)

        try:
            with open(report_file, 'r') as f:
                results = json.load(f)
            print(f"Successfully parsed test report: {report_file}")
            return results
        except FileNotFoundError:
            error_msg = self._handle_missing_report(return_code, stdout, stderr)
            return {"error": error_msg, "exit_code": return_code, "stdout": stdout, "stderr": stderr}
        except json.JSONDecodeError as e:
            return {"error": "Failed to parse JSON report", "details": str(e), "exit_code": return_code}
        except Exception as e:
            return {"error": "Unexpected error handling report", "details": str(e)}

    def _handle_missing_report(self, return_code: int, stdout: str, stderr: str) -> str:
        """Handles cases where the pytest report is missing.
        
        Args:
            return_code: The exit code from pytest
            stdout: Standard output from pytest
            stderr: Standard error from pytest
            
        Returns:
            A descriptive error message
        """
        if return_code == 1:
            return "Tests failed but report file not generated"
        elif return_code == 2:
            return "Pytest command line usage error"
        elif return_code == 3:
            return "Internal pytest error"
        elif return_code == 4:
            return "Pytest was interrupted by user"
        else:
            return f"Unknown error (exit code: {return_code})"

    def analyze_failures(self, test_results: dict, file_path: Optional[str] = None) -> dict:
        """Analyzes test failures using LLM if available.
        
        Args:
            test_results: The parsed pytest results
            file_path: Optional path to the file being tested
            
        Returns:
            Dictionary containing analysis results
        """
        if not self.llm:
            return {"error": "LLM not available for analysis"}
            
        failures = test_results.get("tests", [])
        analysis_results = []
        
        for test in failures:
            if test.get("outcome") == "failed":
                error_msg = test.get("call", {}).get("crash", {}).get("message", "")
                if file_path and self.code_analyzer:
                    code_context = self.code_analyzer.get_code_context(file_path, test.get("nodeid", ""))
                else:
                    code_context = None
                    
                analysis = self.llm.analyze_error(file_path or "", error_msg, code_context)
                analysis_results.append({
                    "test_name": test.get("nodeid"),
                    "error": error_msg,
                    "analysis": analysis
                })
                
        return {"analysis": analysis_results}

    def generate_tests(self, file_path: str, test_file_path: Optional[str] = None) -> dict:
        """Generates test cases for a given file using LLM if available.
        
        Args:
            file_path: Path to the file to generate tests for
            test_file_path: Optional path where to save the generated tests
            
        Returns:
            Dictionary containing generated tests and metadata
        """
        if not self.llm:
            return {"error": "LLM not available for test generation"}
            
        try:
            with open(file_path, 'r') as f:
                code_content = f.read()
                
            suggested_tests = self.llm.suggest_tests(file_path, code_content)
            
            if test_file_path:
                os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
                with open(test_file_path, 'w') as f:
                    f.write(suggested_tests)
                    
            return {
                "file_path": file_path,
                "test_file_path": test_file_path,
                "generated_tests": suggested_tests
            }
        except Exception as e:
            return {"error": f"Failed to generate tests: {str(e)}"}

    def run_test_coverage(self, target: str = ".", cwd: str = None) -> dict:
        """Runs pytest with coverage reporting.
        
        Args:
            target: The file or directory to run tests on
            cwd: The working directory to run pytest from
            
        Returns:
            Dictionary containing coverage results
        """
        coverage_file = os.path.join(self.temp_dir.name, f"coverage_{os.getpid()}.json")
        
        command = [
            sys.executable, "-m", "pytest", target,
            "--cov=" + target,
            f"--cov-report=json:{coverage_file}",
            "--disable-warnings"
        ]
        
        return_code, stdout, stderr = self.executor.run_command(command, cwd=cwd)
        
        try:
            with open(coverage_file, 'r') as f:
                coverage_data = json.load(f)
            return {
                "coverage": coverage_data,
                "exit_code": return_code,
                "stdout": stdout,
                "stderr": stderr
            }
        except Exception as e:
            return {"error": f"Failed to get coverage: {str(e)}"}

    def cleanup(self):
        """Cleans up temporary files and directories."""
        self.temp_dir.cleanup()

    def __del__(self):
        """Ensures cleanup on object destruction."""
        self.cleanup() 