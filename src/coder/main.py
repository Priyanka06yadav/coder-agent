
import warnings
import re
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from coder.crew import Coder
from coder.tools.python_executor import PythonExecutorTool

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
load_dotenv()

MAX_ATTEMPTS = 3


def generate_filename(assignment: str) -> str:
    filename = assignment.lower()
    filename = re.sub(r"[^a-z0-9]+", "_", filename)
    filename = filename.strip("_")[:40]

    return f"{filename}_{uuid4().hex[:8]}.py"


def run_coder(assignment, test_cases_raw, expected_outputs_raw):

    if not assignment.strip():
        return "FAILED", "", "", "Please enter a programming assignment."

    # Convert test cases into stdin format
    test_cases = [
        case.strip().replace(",", "\n") + "\n"
        for case in test_cases_raw.split(";")
        if case.strip()
    ]

    expected_outputs = [
        output.strip()
        for output in expected_outputs_raw.split(";")
        if output.strip()
    ]

    if not test_cases:
        return "FAILED", "", "", "Please provide at least one test case."

    if len(test_cases) != len(expected_outputs):
        return (
            "FAILED",
            "",
            "",
            "Error: Number of test cases and expected outputs must match."
        )

    coder = Coder()
    executor = PythonExecutorTool()

    project_root = Path(__file__).resolve().parents[2]
    sandbox_dir = project_root / "sandbox" / "generated_code"

    filename = generate_filename(assignment)
    file_path = sandbox_dir / filename

    # STEP 1: Generate initial code
    print("\nGenerating Python solution...\n")

    coder.run_task(
        "coding_task",
        {
            "assignment": assignment,
            "filename": filename,
            "sample_input": test_cases_raw
        }
    )

    execution_result = ""
    final_status = "FAILED"

    # STEP 2: Execute and retry
    for attempt in range(1, MAX_ATTEMPTS + 1):

        print(f"\n========== ATTEMPT {attempt} ==========\n")

        test_results = []
        failed_test_details = []

        for i, (test_input, expected_output) in enumerate(
            zip(test_cases, expected_outputs), start=1
        ):

            result = executor.run(
                filename=filename,
                stdin_input=test_input,
                expected_output=expected_output
            )

            test_results.append(result)

            if (
                "Execution Status: SUCCESS" not in result
                or "Correctness Status: CORRECT" not in result
            ):
                failed_test_details.append(
                    {
                        "test_case": i,
                        "input": test_input,
                        "expected_output": expected_output,
                        "execution_result": result
                    }
                )

        execution_result = "\n\n".join(
            f"Test Case {i}:\n{result}"
            for i, result in enumerate(test_results, start=1)
        )

        # All test cases must pass in the current attempt
        if not failed_test_details:
            final_status = "SUCCESS"
            print("\nAll test cases passed!")
            break

        print("\nSome test cases failed.")

        # Prepare feedback containing only failed test cases
        debugging_feedback = "\n\n".join(
            f"""
Test Case: {item['test_case']}
Input:
{item['input']}

Expected Output:
{item['expected_output']}

Actual Execution Result:
{item['execution_result']}
"""
            for item in failed_test_details
        )

        if attempt == MAX_ATTEMPTS:
            print("\nMaximum attempts reached.")
            break

        if not file_path.exists():
            execution_result += "\nGenerated Python file not found."
            break

        previous_code = file_path.read_text(encoding="utf-8")

        print("\nSending failed cases to Coder for debugging...\n")

        coder.run_task(
            "debugging_task",
            {
                "assignment": assignment,
                "filename": filename,
                "previous_code": previous_code,
                "execution_error": debugging_feedback
            }
        )

    # STEP 3: Prepare final report
    final_code = ""

    if file_path.exists():
        final_code = file_path.read_text(encoding="utf-8")

    final_report = (
        f"Filename: {filename}\n"
        f"Execution Status: {final_status}\n"
        f"Maximum Attempts: {MAX_ATTEMPTS}\n\n"
        f"Final Execution Results:\n{execution_result}"
    )

    return final_status, filename, final_code, final_report


if __name__ == "__main__":

    assignment = input("\nWhat Python program should I create? ")

    test_cases = input(
        "\nEnter test cases (separate cases with semicolons): "
    )

    expected_outputs = input(
        "\nEnter expected outputs (separate with semicolons): "
    )

    status, filename, code, report = run_coder(
        assignment,
        test_cases,
        expected_outputs
    )

    print("\n========== FINAL CODER REPORT ==========")
    print(report)
    print("\nFinal Python Code:\n")
    print(code)
