# Coder – AI-Powered Python Coding & Debugging Agent

**Coder** is a project I built to explore how AI agents can automate the process of writing, running, testing, and debugging Python code.

The idea is simple: instead of manually writing a solution and checking every test case, a user can describe a programming problem, provide test cases, and let the agent handle the process.

I used **CrewAI and Gemini** to generate and debug code, Python to manage the workflow, and Docker to run the generated programs in isolated containers. I also built a Gradio interface so the application can be used through a simple web UI.

<img width="929" height="437" alt="Screenshot 2026-11-19 011212" src="https://github.com/user-attachments/assets/91d777b3-9a88-4aaa-b09a-ef5eaf9fdc04" />
<img width="437" height="335" alt="Screenshot 2026-11-19 011240" src="https://github.com/user-attachments/assets/a1a769bf-6ae6-470f-becb-d1d9d2dabcde" />
<img width="452" height="423" alt="Screenshot 2026-11-19 011223" src="https://github.com/user-attachments/assets/4b53fd7e-e3e6-4226-ae86-faa739407eee" />


## What can it do?

- Generate Python solutions from natural-language programming assignments.
- Accept multiple test cases and their expected outputs.
- Run generated code inside Docker containers instead of executing it directly in the main application.
- Compare actual outputs with expected outputs to identify failures.
- Send failed test cases and execution details to an AI debugging task.
- Retry the solution after debugging, with a maximum of three attempts.
- Display the final code, execution status, and test results through Gradio.

## How I built it

I wanted to keep code generation, execution, and debugging as separate responsibilities rather than putting everything into one agent.

The application uses two CrewAI tasks:

- **Coding task:** Understands the assignment and generates the initial Python solution.
- **Debugging task:** Looks at the previous code and failed test cases, identifies the issue, and updates the solution.

I also developed two custom tools:

- **FileWriterTool:** Saves generated Python code to the project's sandbox directory.
- **PythonExecutorTool:** Runs the generated file inside a Docker container and captures its output, errors, and exit code.

One important part of the workflow is that after debugging, I run the entire test suite again, not just the previously failed cases. This helps catch situations where fixing one test case accidentally breaks another.

## How the workflow works

```text
User submits assignment and test cases
                  |
                  v
          CrewAI Coding Task
                  |
                  v
          Generate Python Code
                  |
                  v
            FileWriterTool
                  |
                  v
          Save Generated File
                  |
                  v
          PythonExecutorTool
                  |
                  v
           Docker Execution
                  |
                  v
       Compare Actual vs Expected
                  |
             Are all tests passing?
                /       \
              Yes        No
               |          |
               v          v
          Final Report  Debugging Task
                            |
                            v
                       Fix the Code
                            |
                            v
                    Run All Tests Again
```

The workflow stops when all test cases pass or after three execution attempts.

## Tech Stack

| Technology | How I used it |
|---|---|
| Python | Main application logic and workflow |
| CrewAI | Managing coding and debugging tasks |
| Gemini | Generating and debugging Python code |
| Docker | Running generated code in containers |
| Gradio | Building the web interface |
| uv | Managing dependencies and the Python environment |

## Project Structure

```text
coder/
│
├── src/
│   └── coder/
│       ├── main.py
│       ├── crew.py
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── tools/
│           ├── file_writer.py
│           └── python_executor.py
│
├── sandbox/
│   └── generated_code/
│
├── app.py
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
└── README.md
```

## Running the project locally

### Prerequisites

Make sure you have the following installed:

- Python 3.12
- Docker Desktop
- Git
- uv
- A Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Set up environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Add your Gemini API key and any other required configuration values.

Keep your actual `.env` file private. Never upload API keys to GitHub.

### 4. Build the Docker image

```bash
docker build -t coder-python-runner .
```

Make sure Docker Desktop is running and its Linux container engine is available.

### 5. Start the application

```bash
uv run python app.py
```

Open the local Gradio URL in your browser:

```text
http://127.0.0.1:7860
```

## Example

Try giving Coder this assignment:

**Assignment:**

Write a Python program to find the sum of two numbers.

**Test cases:**

```text
10,20; 5,7; -2,5
```

**Expected outputs:**

```text
30; 12; 3
```

Coder generates the solution, runs it against the supplied test cases, and displays the results along with the generated Python code.

## What I'm planning to improve

There are still a few things I'd like to explore further:

- Improve the interface and show more detailed execution progress.
- Support additional programming languages.
- Add support for more flexible test-case formats.
- Store previous coding sessions and execution history.
- Improve debugging and execution reports.

---

**Built as a hands-on project to learn more about AI agents, tool calling, workflow orchestration, and automated code execution.**
