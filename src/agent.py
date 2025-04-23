from .debugger import Debugger
from .test_runner import TestRunner
# We might need CodeAnalyzer and Executor if Agent interacts directly,
# but for now, they are dependencies of Debugger/TestRunner.

class Agent:
    """Represents the core AI Agent that can debug and test code."""

    def __init__(self, debugger: Debugger, test_runner: TestRunner, config=None):
        """Initialize the agent with necessary components and optional configuration."""
        self.config = config or {}
        self.debugger = debugger
        self.test_runner = test_runner
        print("Agent initialized with Debugger and TestRunner.")

    def run(self):
        """Run the main agent loop or task. Placeholder implementation."""
        print("Agent is running... Waiting for tasks.")
        # TODO: Implement the main loop, potentially reading tasks from a queue or user input.
        # Example task handling (replace with actual logic):
        # task = self.get_next_task()
        # if task.type == 'debug':
        #     self.debug_code(task.file_path)
        # elif task.type == 'test':
        #     self.run_tests(task.target)

    def debug_code(self, file_path: str):
        """Triggers the debugging process for a given file."""
        print(f"\n--- Agent Task: Debug Code --- ")
        print(f"File to debug: {file_path}")
        self.debugger.debug_file(file_path)
        print("------------------------------\n")

    def run_tests(self, target: str):
        """Triggers the test running process for a given target."""
        print(f"\n--- Agent Task: Run Tests --- ")
        print(f"Target for tests: {target}")
        test_results = self.test_runner.run_pytest(target=target)
        # TODO: Process test_results (e.g., report summary, use LLM for failures)
        print("Test Results Summary:")
        if isinstance(test_results, dict) and 'summary' in test_results:
            print(f"  Passed: {test_results['summary'].get('passed', 0)}")
            print(f"  Failed: {test_results['summary'].get('failed', 0)}")
            print(f"  Errors: {test_results['summary'].get('error', 0)}") # Note: key might be 'errors'
            print(f"  Skipped: {test_results['summary'].get('skipped', 0)}")
            print(f"  Total: {test_results['summary'].get('total', 0)}")
        elif isinstance(test_results, dict) and 'error' in test_results:
            print(f"  Error running tests: {test_results['error']}")
        else:
            print("  Could not parse test summary from results.")
            print(f"Raw results: {test_results}")
        print("---------------------------\n")

    # Add more methods as needed for specific agent capabilities
    # e.g., process_input, generate_response, learn, etc. 