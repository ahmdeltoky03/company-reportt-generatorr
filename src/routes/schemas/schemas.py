from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class APIKeysRequest(BaseModel):
  cohere_api_key: str
  tavily_api_key: str
  
class CompanyReportRequest(BaseModel):
  """Request model for company report generation"""
  company_name: str
  company_link: Optional[str] = None
  