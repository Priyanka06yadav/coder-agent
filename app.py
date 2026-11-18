import gradio as gr
from coder.main import run_coder


def generate_solution(assignment, test_cases, expected_outputs):

    status, filename, code, report = run_coder(
        assignment,
        test_cases,
        expected_outputs
    )

    return status, filename, code, report


with gr.Blocks(title="Coder - AI Python Developer") as demo:

    gr.Markdown(
        """
        # 🧑‍💻 Coder
        ### AI-Powered Python Coding and Debugging Assistant

        Describe your programming problem, provide test cases,
        and let the AI agent generate, execute and debug your solution.
        """
    )

    with gr.Row():

        with gr.Column(scale=1):

            assignment = gr.Textbox(
                label="Programming Assignment",
                placeholder="Write a Python program to find the sum of two numbers.",
                lines=4
            )

            test_cases = gr.Textbox(
                label="Test Cases",
                placeholder="10,20; 5,7; -2,5",
                lines=3
            )

            expected_outputs = gr.Textbox(
                label="Expected Outputs",
                placeholder="30; 12; 3",
                lines=3
            )

            generate_button = gr.Button(
                "Generate & Run",
                variant="primary"
            )

        with gr.Column(scale=1):

            status = gr.Textbox(
                label="Execution Status",
                interactive=False
            )

            filename = gr.Textbox(
                label="Generated Filename",
                interactive=False
            )

            generated_code = gr.Code(
                label="Generated Python Code",
                language="python",
                interactive=False
            )

    report = gr.Textbox(
        label="Execution Report",
        lines=12,
        interactive=False
    )

    generate_button.click(
        fn=generate_solution,
        inputs=[
            assignment,
            test_cases,
            expected_outputs
        ],
        outputs=[
            status,
            filename,
            generated_code,
            report
        ]
    )


if __name__ == "__main__":
    demo.launch()
