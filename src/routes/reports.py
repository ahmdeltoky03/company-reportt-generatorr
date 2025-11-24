from fastapi import APIRouter, HTTPException

from src.models.schemas import  CompanyReportResponse
from .schemas import CompanyReportRequest
from src.services.report_generator import ReportGeneratorService
from src.routes.keys import get_api_keys
from src.config import settings


router = APIRouter(prefix="/api/report", tags=["reports"])


@router.post("/generate", response_model=CompanyReportResponse)
async def generate_report(request: CompanyReportRequest):
    """Generate a structured company report"""
    try:
        api_keys = get_api_keys()
        
        if "cohere" not in api_keys or "tavily" not in api_keys:
            raise HTTPException(
                status_code=400,
                detail="API keys not set. Please set your API keys first."
            )
        
        report_service = ReportGeneratorService(
            cohere_api_key=api_keys["cohere"],
            tavily_api_key=api_keys["tavily"],
            agentops_api_key=settings.agentops_api_key
        )
        
        structured_report = report_service.generate_company_report(
            company_name=request.company_name,
            company_link=request.company_link
        )
        
        return CompanyReportResponse(
            company_name=request.company_name,
            report=structured_report
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")