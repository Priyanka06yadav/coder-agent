from pathlib import Path
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# 1. Define the input schema
class FileWriterInput(BaseModel):
    filename: str = Field(
        description= "Name of the Python file to create, e.g. factorial.py"
    )

    code: str = Field(
        description="Complete Python source code to save in the file"
    )

# 2. Create the custom tool
class FileWriterTool(BaseTool):

    name: str = "Python File Writer"
    description: str = (
        "Creates a Python file and saves the provided source code"
        "inside the sandbox/generated_code directory."
        "Use this tool after generating the complete Python solution."
    )

    args_schema: type[BaseModel] = FileWriterInput

    def _run(self, filename: str, code: str) -> str:

        # Locate the project root
        project_root = Path(__file__).resolve().parents[3]

        # Define the sandbox directory
        output_dir = project_root / "sandbox" / "generated_code"

        # Validate filename
        if Path(filename).name != filename:
            return "Error: Only a filename is allowed. Directory paths are not permitted."

        if not filename.endswith(".py"):
            return "Error: Only Python files (.py) are allowed."

        if not filename[:-3].strip():
            return "Error: Filename cannot be empty."

        try:
            # Create directory if it doesn't exist
            output_dir.mkdir(parents=True, exist_ok=True)

            # Create and write the Python file
            file_path = output_dir / filename
            file_path.write_text(code, encoding="utf-8")

            return f"Success: Python file created at {file_path}"

        except OSError as error:
            return f"File creation failed: {error}"




