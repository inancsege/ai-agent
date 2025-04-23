import argparse
import os
from dotenv import load_dotenv

from .agent import Agent
from .code_analyzer import CodeAnalyzer
from .debugger import Debugger
from .executor import Executor
from .llm_interface import LLMInterface # Placeholder
from .test_runner import TestRunner

def main():
    """Main function to initialize components and run the agent."""
    load_dotenv() # Load environment variables from .env file

    # --- Configuration Loading (Example) ---
    # TODO: Implement more robust config loading (e.g., YAML file, command line args)
    config = {
        "llm_api_key": os.getenv("OPENAI_API_KEY"), # Example: Load API key
        "llm_model_name": os.getenv("LLM_MODEL_NAME", "gpt-4o-mini") # Example model
    }
    print("Configuration loaded.")

    # --- Argument Parsing (Example) ---
    parser = argparse.ArgumentParser(description="AI Agent for Code Debugging and Testing.")
    parser.add_argument("--debug", metavar="FILE_PATH", help="Run the debugger on the specified Python file.")
    parser.add_argument("--test", metavar="TARGET", nargs='?', const=".", default=None, help="Run tests on the specified target (file or directory, defaults to current directory if flag is present with no value).")
    # Add other arguments as needed (e.g., --config-file)
    args = parser.parse_args()

    # --- Component Initialization ---
    # Initialize components needed by the agent
    # Note: LLMInterface is currently a placeholder
    llm_interface = LLMInterface(api_key=config.get("llm_api_key"), model_name=config.get("llm_model_name"))
    code_analyzer = CodeAnalyzer()
    executor = Executor()
    # Inject dependencies
    # TODO: Inject llm_interface into Debugger/TestRunner when implemented
    debugger = Debugger(executor=executor, analyzer=code_analyzer)
    test_runner = TestRunner(executor=executor)

    # --- Agent Initialization ---
    agent = Agent(
        debugger=debugger,
        test_runner=test_runner,
        config=config
    )

    # --- Task Execution based on Args ---
    if args.debug:
        agent.debug_code(args.debug)
    elif args.test is not None: # Check if --test flag was used (even without a value)
        agent.run_tests(args.test)
    else:
        # Default behavior if no specific task is given
        print("No specific task provided via arguments. Starting default agent run...")
        agent.run() # Run the default agent behavior (currently just prints)

if __name__ == "__main__":
    # This allows running the script directly for development/testing,
    # but it's often better to run modules using python -m src.main
    print("Running main script directly...")
    main() 