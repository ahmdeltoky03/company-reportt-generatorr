from typing import Optional
from src.services.tavily_service import TavilySearchService
from src.agents.crew import CompanyReportCrew
from src.models.schemas import StructuredCompanyReport
from pydantic import ValidationError
import json


class ReportGeneratorService:
    """Service that orchestrates report generation using CrewAI agents"""
    
    def __init__(self, cohere_api_key: str, tavily_api_key: str, agentops_api_key: str = None, model_id: str = "command-a-03-2025"):
        """Initialize report generator service"""
        self.tavily_service = TavilySearchService(tavily_api_key=tavily_api_key)
        self.crew = CompanyReportCrew(cohere_api_key=cohere_api_key, agentops_api_key=agentops_api_key, model_id=model_id)
    
    def generate_company_report(self, company_name: str, company_link: Optional[str] = None) -> StructuredCompanyReport:
        """Generate a complete structured company report"""
        try:
            print(f"\n{'='*60}")
            print(f"## Starting report generation for {company_name}...")
            print(f"{'='*60}\n")
            
            print(f"## STEP 1 Searching for comprehensive information about {company_name}...")
            company_details = self.tavily_service.get_company_details(company_name, company_link)
            raw_content = company_details.get("raw_content", "")
            sources = company_details.get("sources", [])
            
            # print(f"## SUCCESS Found comprehensive company information from {len(sources)} sources\n")
            print(f"{'-'*60}\n")
            
            print(f"## STEP 2 Generating structured report using AI agents...")
            report_dict = self.crew.generate_report(company_name, raw_content)
            
            if isinstance(report_dict, str):
                # print(f"## WARNING Report is string, converting to dict ")
                try:
                    json_str = report_dict
                    if "```json" in json_str:
                        json_str = json_str.split("```json")[1].split("```")[0]
                    elif "```" in json_str:
                        json_str = json_str.split("```")[1].split("```")[0]
                    report_dict = json.loads(json_str.strip())
                except:
                    # print(f"## ERROR Could not convert string to dict")
                    return self._create_fallback_report(company_name)
            
            if not isinstance(report_dict, dict):
                report_dict = {}
            
            if isinstance(report_dict, dict) and "references" in report_dict:
                if isinstance(report_dict["references"], dict):
                    existing_refs = report_dict["references"].get("references", [])
                    for source in sources:
                        if source not in existing_refs:
                            existing_refs.append(source)
                    report_dict["references"]["references"] = existing_refs[:15]
                else:
                    report_dict["references"] = {
                        "references": sources[:15] if sources else [{"source_name": "Research", "url": "https://example.com"}]
                    }
            else:
                report_dict["references"] = {
                    "references": sources[:15] if sources else [{"source_name": "Research", "url": "https://example.com"}]
                }
            
            print(f"## STEP 3 Validating report against schema...")
            try:
                structured_report = StructuredCompanyReport.parse_obj(report_dict)
                print(f"## SUCCESS Report validated successfully\n")
            except ValidationError as ve:
                print(f"## WARNING Validation error: {ve}")
                structured_report = StructuredCompanyReport.parse_obj(report_dict)
            
            print(f"{'='*60}")
            print(f"## Report generation completed successfully!")
            print(f"{'='*60}\n")
            
            return structured_report
            
        except Exception as e:
            print(f"\n## ERROR Report generation failed: {str(e)}\n")
            import traceback
            traceback.print_exc()
            raise Exception(f"Error generating report for {company_name}: {str(e)}")
    
    def _create_fallback_report(self, company_name: str) -> StructuredCompanyReport:
      """Create a fallback report """
      return StructuredCompanyReport.create_fallback(company_name)