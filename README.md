# AI Test Agent

An intelligent AI-powered agent for automated testing, debugging, and code analysis.

## Description

The AI Test Agent is a sophisticated tool that combines traditional testing frameworks with AI capabilities to provide comprehensive code testing and debugging solutions. It leverages Large Language Models (LLMs) to analyze test failures, generate test cases, and provide intelligent debugging assistance.

### Key Features

- **Automated Test Execution**: Run and manage unit tests using pytest with detailed reporting
- **AI-Powered Test Analysis**: Get intelligent insights into test failures using LLM analysis
- **Smart Test Generation**: Automatically generate relevant test cases for your code
- **Code Coverage Analysis**: Track and analyze code coverage metrics
- **Intelligent Debugging**: Receive AI-powered suggestions for fixing test failures
- **Temporary File Management**: Automatic cleanup of test artifacts and reports
- **Customizable Test Configuration**: Flexible test running with custom pytest arguments

## Getting Started

### Prerequisites

*   Python 3.8 or higher
*   pip (Python package installer)
*   pytest (for running tests)
*   pytest-cov (for coverage reporting)
*   pytest-json-report (for JSON test reports)

### Installation

1.  Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd ai-agent-
    ```

2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Basic Test Running

```python
from ai_filtering_comparison.src import TestRunner
from ai_filtering_comparison.src import Executor
from ai_filtering_comparison.src import LLMInterface

# Initialize components
executor = Executor()
llm = LLMInterface(api_key="your-api-key")  # Optional
test_runner = TestRunner(executor, llm)

# Run tests
results = test_runner.run_pytest("path/to/tests")
```

### Advanced Features

#### Test Failure Analysis

```python
# Get AI-powered analysis of test failures
analysis = test_runner.analyze_failures(results, "path/to/source/file.py")
```

#### Test Generation

```python
# Generate new test cases
generated_tests = test_runner.generate_tests(
    "path/to/source/file.py",
    "path/to/save/tests.py"
)
```

#### Coverage Analysis

```python
# Run tests with coverage reporting
coverage = test_runner.run_test_coverage("path/to/tests")
```

### Configuration Options

The TestRunner supports various configuration options:

- Custom pytest arguments
- Working directory specification
- Test target selection
- Coverage reporting
- LLM integration for advanced analysis

## Architecture

The AI Test Agent consists of several key components:

1. **TestRunner**: Core component for running tests and managing test artifacts
2. **Executor**: Handles command execution and process management
3. **LLMInterface**: Manages interactions with Large Language Models
4. **CodeAnalyzer**: Provides code context and analysis capabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.