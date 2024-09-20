from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from stock_analysis.tools.calculator_tool import CalculatorTool
from stock_analysis.tools.sec_tools import SEC10KTool, SEC10QTool

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool

from langchain_community.llms import Ollama


class StockAnalysisAgents():

    def __ini__(self):
        self.llm = Ollama(model="openhermes")
        self.CalculationTool = CalculatorTool()
        self.SEC10KTool = SEC10KTool("AMZN")
        self.SEC10QTool = SEC10QTool("AMZN")
        self.ScrapeWebsiteTool = ScrapeWebsiteTool()
        self.WebsiteSearchTool = WebsiteSearchTool()
        self.TXTSearchTool = TXTSearchTool()
        self.agents_config = 'config/agents.yaml'


    def financial_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            llm=self.llm,
            tools=[
                self.ScrapeWebsiteTool,
                self.WebsiteSearchTool,
                self.CalculationTool,
                self.SEC10QTool,
                self.SEC10KTool,
            ]
        )
    
    def research_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_analyst'],
            verbose=True,
            llm=self.llm,
            tools=[
                self.ScrapeWebsiteTool,
                # WebsiteSearchTool(), 
                self.SEC10QTool,
                self.SEC10KTool,
            ]
        )
    
    def financial_analyst_agents(self) -> List[Agent]:
        return [self.financial_agent(), self.research_analyst_agent()]
    

    def investment_advisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_advisor'],
            verbose=True,
            llm=self.llm,
            tools=[
                self.ScrapeWebsiteTool,
                self.WebsiteSearchTool,
                self.CalculationTool,
                self.SEC10QTool,
                self.SEC10KTool,
            ]
        )
    
