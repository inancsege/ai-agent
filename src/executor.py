import subprocess
import sys

class Executor:
    """Executes external commands and scripts."""

    def __init__(self):
        pass

    def run_command(self, command: list[str], cwd: str = None) -> tuple[int, str, str]:
        """Runs an external command and returns return code, stdout, and stderr."""
        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,  # Don't raise exception for non-zero exit codes
                cwd=cwd
            )
            return process.returncode, process.stdout, process.stderr
        except FileNotFoundError:
            print(f"Error: Command not found: {command[0]}")
            # Re-raise or handle as appropriate
            raise
        except Exception as e:
            print(f"An unexpected error occurred while running command {' '.join(command)}: {e}")
            raise

    def run_python_script(self, script_path: str, args: list[str] = None, cwd: str = None) -> tuple[int, str, str]:
        """Runs a specific Python script."""
        command = [sys.executable, script_path]
        if args:
            command.extend(args)
        return self.run_command(command, cwd=cwd)

    # TODO: Add methods for specific execution environments if needed 