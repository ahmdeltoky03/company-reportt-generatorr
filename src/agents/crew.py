from crewai import Crew
from langchain_cohere import ChatCohere
import json
import os
from datetime import datetime
from .research_agent import ResearchAgent
from .analysis_agent import AnalysisAgent
from .writer_agent import WriterAgent
import random, string


class CompanyReportCrew:
    """Orchestrates multiple AI agents to generate comprehensive company reports"""
    
    def __init__(self, cohere_api_key: str, agentops_api_key: str = None, model_id: str = "command-a-03-2025"):
        """Initialize crew with LLM and agent instances, create assets directory"""
        
        if not cohere_api_key or cohere_api_key.strip() == "":
            raise ValueError("Cohere API key is required and cannot be empty")
        
        os.environ["COHERE_API_KEY"] = cohere_api_key
        
        self.llm = ChatCohere(model=model_id)
        
        self.research_agent_class = ResearchAgent(self.llm)
        self.analysis_agent_class = AnalysisAgent(self.llm)
        self.writer_agent_class = WriterAgent(self.llm)
        
        self.output_dir = "src/assets"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
          
    
    
    def generate_report(self, company_name: str, company_data: str) -> str:
        """Execute crew pipeline with three agents and save outputs to assets folder"""
        try:
            print(f"## CREW Starting crew execution for {company_name}")
            
            research_agent = self.research_agent_class.create_agent()
            analysis_agent = self.analysis_agent_class.create_agent()
            writer_agent = self.writer_agent_class.create_agent()
            
            research_task = self.research_agent_class.create_task(research_agent, company_data)
            analysis_task = self.analysis_agent_class.create_task(analysis_agent, research_task.output)
            report_task = self.writer_agent_class.create_task(writer_agent, company_name, analysis_task.output)
            
            crew = Crew(
                agents=[research_agent, analysis_agent, writer_agent],
                tasks=[research_task, analysis_task, report_task],
                verbose=True
            )
            
            result = crew.kickoff()
            report_text = str(result) if result else ""
            
            if not report_text or report_text.strip() == "":
                report_text = f"# {company_name}\n\nReport generation completed."
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            
            self.report_dir = os.path.join(self.output_dir, f"{company_name}_{self.generate_random_string()}") 
            
            if not os.path.exists(self.report_dir):
                os.makedirs(self.report_dir)
                
            research_data = {
                "agent": "research_agent",
                "company": company_name,
                "output": str(research_task.output)
            }
            with open(f"{self.report_dir}/research.json", "w") as f:
                json.dump(research_data, f, indent=2)
            print(f"## CREW Saved research_agent output to src/assets/")
            
            analysis_data = {
                "agent": "analysis_agent",
                "company": company_name,
                "output": str(analysis_task.output)
            }
            with open(f"{self.report_dir}/analysis.json", "w") as f:
                json.dump(analysis_data, f, indent=2)
            print(f"## CREW Saved analysis_agent output to src/assets/")
            
            writer_data = {
                "agent": "writer_agent",
                "company": company_name,
                "output": report_text
            }
            with open(f"{self.report_dir}/writer.json", "w") as f:
                json.dump(writer_data, f, indent=2)
            print(f"## CREW Saved writer_agent output to src/assets/")
            
            print(f"## CREW Crew execution completed successfully for {company_name}")
            
            return report_text
            
        except Exception as e:
            print(f"## CREW ERROR {str(e)}")
            raise Exception(f"Crew execution error: {str(e)}")
    
    def generate_random_string(self, length : int=12):
      return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))