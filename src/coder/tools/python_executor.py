import subprocess
import sys
from pathlib import Path
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from uuid import uuid4

MAX_INPUT_CHARS = 10_000
MAX_OUTPUT_CHARS = 10_000
MAX_CODE_FILE_BYTES = 100_000

# 1. Define input schema
class PythonExecutorInput(BaseModel):

    filename: str = Field(
        description= "Name of the Python file to execute, e.g. factorial.py"
    )

    stdin_input: str = Field(
        default="",
        description="Optional input to pass to the Python program through stddin"
    )

    expected_output: str = Field(
        default="",
        description="Expected output of the program for correctness validation"
    )

# 2. Create custom execution tool
class PythonExecutorTool(BaseTool):

    name: str = "Python Code Executor"
    description: str = (
        "Executes a previously generated Python file from the sandbox directory."
        "Returns standard output, errors, and execution status."
        "Can also pass input to programs that use input()."
    )

    args_schema: type[BaseModel] = PythonExecutorInput

    def _run(self, filename: str, stdin_input: str = "", expected_output: str = "") -> str:

        # Locate project root
        project_root = Path(__file__).resolve().parents[3]

        # Locate generated code directory
        sandbox_dir = project_root / "sandbox" / "generated_code"

        # Validate filename
        if Path(filename).name != filename or not filename.endswith(".py"):
            return "Error: Only a Python filename is allowed."

        if not filename[:-3].strip():
            return "Error: Filename cannot be empty."

        file_path = sandbox_dir / filename

        # Check whether file exists
        if not file_path.is_file():
            return f"Error: File not found: {filename}"

        if len(stdin_input) > MAX_INPUT_CHARS:
            return (
                f"Execution rejected: Input is too large. "
                f"Maximum allowed input is {MAX_INPUT_CHARS} characters."
            )

        if file_path.stat().st_size > MAX_CODE_FILE_BYTES:
            return (
                "Execution rejected: Python file is too large. "
                f"Maximum allowed size is {MAX_CODE_FILE_BYTES} bytes."
            )

        container_name = f"coder-runner-{uuid4().hex[:12]}"

        try:
            # Execute Python file
            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",

                    "--name", container_name,

                    "-i",
                    "--network", "none",
                    "--memory", "128m",
                    "--cpus", "0.5",
                    "--read-only",
                    "--pids-limit", "64",
                    "--cap-drop", "ALL",
                    "--security-opt", "no-new-privileges",
                    "--user", "1000:1000",

                    "--mount",
                    f"type=bind,source={sandbox_dir.resolve()},target=/app,readonly",

                    "--workdir", "/app",

                    "coder-python-runner",
                    "python",
                    filename
                ],
                capture_output=True,
                text=True,
                input=stdin_input,
                timeout=10
            )

            stdout = result.stdout[:MAX_OUTPUT_CHARS]
            stderr = result.stderr[:MAX_OUTPUT_CHARS]

            if len(result.stdout) > MAX_OUTPUT_CHARS:
                stdout += "\n[Output truncated: maximum output limit reached]"

            if len(result.stderr) > MAX_OUTPUT_CHARS:
                stderr += "\n[Error output truncated: maximum output limit reached]"

            execution_status = "SUCCESS" if result.returncode == 0 else "FAILED"

            correctness_status = "NOT CHECKED"

            if result.returncode == 0 and expected_output.strip():
                if result.stdout.strip() == expected_output.strip():
                    correctness_status = "CORRECT"
                else:
                    correctness_status = "INCORRECT"

            return (
                f"Execution Status: {execution_status}\n"
                f"Correctness Status: {correctness_status}\n"
                f"Exit Code: {result.returncode}\n"
                f"Standard Output:\n{stdout}\n"
                f"Standard Error:\n{stderr}"
                )

        except subprocess.TimeoutExpired:
            try:
                subprocess.run(
                    ["docker", "kill", container_name],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            except (subprocess.TimeoutExpired, OSError):
                pass

            return (
                "Execution Status: FAILED\n"
                "Error: Execution timed out after 10 seconds."
            )



