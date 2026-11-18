from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from coder.tools.file_writer import FileWriterTool
from coder.tools.python_executor import PythonExecutorTool

@CrewBase
class Coder():
    """Coder crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config["coder"],
            tools = [
                FileWriterTool(),
                PythonExecutorTool()
                ],
            verbose=True
        )

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config["coding_task"]
        )

    @task
    def debugging_task(self) -> Task:
        return Task(
            config=self.tasks_config["debugging_task"]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Coder crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    def run_task(self, task_name: str, inputs: dict):
        agent = Agent(
            config=self.agents_config["coder"],
            tools=[
                FileWriterTool(),
                PythonExecutorTool()
            ],
            verbose=True
        )

        task = Task(
            config=self.tasks_config[task_name],
            agent=agent
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff(inputs=inputs)
