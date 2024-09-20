from crewai import Task, Agent
from textwrap import dedent
from log_manager import append_event


class StockAnalysisTask():

    def __init__(self, input_id):
        self.stock = input_id
        self.tasks_config = 'config/tasks.yaml'

    def append_event_callback(self, task_output):
        print(f"Appending event for {self.input_id} with output {task_output}")
        append_event(self.input_id, task_output.exported_output)

    def financial(self,agent:Agent, company_stock: list[str]) -> Task:
        return Task(
            config=self.tasks_config['financial_analysis'],
            agent=agent,
            arguments=company_stock,
            callback=self.append_event_callback,
        )
    
    def research(self, agent:Agent, company_stock: list[str]) -> Task:
        return Task(
            config=self.tasks_config['research'],
            agent=agent,
            arguments=company_stock,
            callback=self.append_event_callback,
        )
    
    def financial_analysis(self, agent:Agent, company_stock: list[str]) -> Task:
        return Task(
            config=self.tasks_config['financial_analysis'],
            agent=agent,
            arguments=company_stock,
            callback=self.append_event_callback,
        )
    
    def filings_analysis(self, agent:Agent, company_stock: list[str]) -> Task:
        return Task(
            config=self.tasks_config['filings_analysis'],
            agent=agent,
            arguments=company_stock,
            callback=self.append_event_callback,
        )
    
    def recommend(self, agent:Agent) -> Task:
        return Task(
            config=self.tasks_config['recommend'],
            agent=agent,
            callback=self.append_event_callback,
        )
    
