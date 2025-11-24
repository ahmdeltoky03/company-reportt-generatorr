from crewai import Agent, Task
from langchain_cohere import ChatCohere
from src.models.schemas import StructuredCompanyReport
import json


class WriterAgent:
    """Converts structured company analysis into JSON format matching schema"""
    
    def __init__(self, llm: ChatCohere):
        self.llm = llm
    
    def create_agent(self) -> Agent:
        """Create and return writer agent"""
        return Agent(
            role="JSON Report Generator",
            goal="Convert detailed company analysis into perfectly structured JSON matching the schema",
            backstory="Expert at creating well-formatted JSON reports with accurate data mapping.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_task(self, agent: Agent, company_name: str, analysis: str) -> Task:
        """Create task to generate JSON structured report matching Pydantic schema exactly"""
        
        schema = json.dumps(StructuredCompanyReport.model_json_schema(), indent=2)
        example = json.dumps(StructuredCompanyReport.model_config.get('json_schema_extra', {}).get('example'), indent=2)
        
        return Task(
            description=f"""Generate a structured company report JSON for {company_name} based on this analysis:

{analysis}

Follow EXACTLY this Pydantic schema structure:

{schema}

Use this example as reference for formatting:

{example}

Generate ONLY valid JSON output - no markdown, no explanations, no code blocks.
Start with opening brace and end with closing brace.""",
            agent=agent,
            expected_output="Valid JSON matching the StructuredCompanyReport schema exactly as provided"
        )