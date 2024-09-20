from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from stock_analysis.tools.calculator_tool import CalculatorTool
from stock_analysis.tools.sec_tools import SEC10KTool, SEC10QTool

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool

from langchain_community.llms import Ollama

from tasks import StockAnalysisTask
from agents import StockAnalysisAgents

from log_manager import append_event


class StockAnalysisCrew:

    def __init__(self, input_id):
        self.llm = Ollama(model="openhermes")
        self.input_id = input_id
        self.crew = None
        
    def setup_crew(self,company_stock: list[str]):
        print("Setting up crew form stock analysis with company stock: ", company_stock)

        agents = StockAnalysisAgents()

        financial_agent = agents.financial_agent()
        research_analyst_agent = agents.research_analyst_agent()
        financial_analyst_agents = agents.financial_analyst_agents()
        investment_advisor_agent = agents.investment_advisor_agent()

        tasks = StockAnalysisTask(self.input_id)

        financial = tasks.financial_analysis(
            financial_agent, company_stock
        )

        research = tasks.research(
            research_analyst_agent, company_stock
        )

        financial_analysis = tasks.financial_analysis(
            financial_analyst_agents, company_stock
        )

        filings_analysis = tasks.filings_analysis(
            financial_analyst_agents, company_stock
        )

        recommend = tasks.recommend(
            investment_advisor_agent
        )

        self.crew = Crew(
            agents=[financial_agent, research_analyst_agent],
            tasks=[financial, research, financial_analysis, filings_analysis, recommend],
            verbose=2
        )

    def kickoff(self):
        if not self.crew:
            print("Crew has not been set up")
            return
        
        append_event(self.input_id, "Crew has been set up, starting crew now.")

        try:
            print("Starting crew")
            results = self.crew.kickoff()
            append_event(self.input_id, "Crew has finished running.")
            return results
        except Exception as e:
            append_event(self.input_id, "Crew has failed to run.")
            return str(e)
   
        