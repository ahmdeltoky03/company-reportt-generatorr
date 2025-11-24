from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class Leader(BaseModel):
    name: str = Field(..., description="Leader full name")
    role: str = Field(..., description="Leader position or title")


class ProductService(BaseModel):
    name: str = Field(..., description="Name of the product or service")
    description: Optional[str] = Field(None, description="Short description if available")


class CompetitiveAdvantage(BaseModel):
    point: str = Field(..., min_length=5)


class FundingRound(BaseModel):
    round_type: Optional[str] = Field(None)
    amount: Optional[str] = Field(None)
    date: Optional[str] = Field(None)
    investors: Optional[List[str]] = Field(default_factory=list)


class NewsItem(BaseModel):
    title: str = Field(..., description="Headline or title")
    summary: Optional[str] = Field(None, description="Optional short summary")
    date: Optional[str] = None


class Reference(BaseModel):
    source_name: str = Field(..., description="Publisher or website")
    url: str = Field(..., description="URL of the source")


class CompanyOverview(BaseModel):
    business_description: str
    core_products_and_services: List[str] = Field(..., min_items=1)
    leadership_team: List[Leader] = Field(..., min_items=1)
    target_market: Optional[str] = None
    competitive_advantages: List[CompetitiveAdvantage]
    business_model: Optional[str] = None
    funding_and_investment: Optional[str] = None
    
    @field_validator('business_description', mode='before')
    @classmethod
    def validate_business_description(cls, v):
        """Ensure business description is not empty"""
        if not v or (isinstance(v, str) and not v.strip()):
            return "Information not available"
        return v
    
    @field_validator('core_products_and_services', mode='before')
    @classmethod
    def validate_products(cls, v):
        """Ensure products list is never empty"""
        if not v or len(v) == 0:
            return ["Product/Service"]
        return v
    
    @field_validator('leadership_team', mode='before')
    @classmethod
    def validate_leadership(cls, v):
        """Ensure leadership team is never empty"""
        if not v or len(v) == 0:
            return [{"name": "Unknown", "role": "Leadership"}]
        return v
    
    @field_validator('competitive_advantages', mode='before')
    @classmethod
    def validate_advantages(cls, v):
        """Ensure competitive advantages list is never empty"""
        if not v or len(v) == 0:
            return [{"point": "Market presence"}]
        return v


class IndustryOverview(BaseModel):
    market_landscape: str
    competition: List[str] = Field(..., min_items=1)
    market_challenges: Optional[str] = None
    
    @field_validator('market_landscape', mode='before')
    @classmethod
    def validate_landscape(cls, v):
        """Ensure market landscape is not empty"""
        if not v or (isinstance(v, str) and not v.strip()):
            return "Information not available"
        return v
    
    @field_validator('competition', mode='before')
    @classmethod
    def validate_competition(cls, v):
        """Ensure competition list is never empty"""
        if not v or len(v) == 0:
            return ["Competitor A", "Competitor B"]
        return v
    
    @field_validator('market_challenges', mode='before')
    @classmethod
    def validate_challenges(cls, v):
        """Ensure market challenges default value"""
        if not v or (isinstance(v, str) and not v.strip()):
            return "Information not available"
        return v


class FinancialOverview(BaseModel):
    revenue_model: str
    revenue_2024: Optional[str] = None
    growth_rate: Optional[str] = None
    net_income_change: Optional[str] = None
    key_metrics: Optional[List[str]] = None
    
    @field_validator('revenue_model', mode='before')
    @classmethod
    def validate_revenue_model(cls, v):
        """Ensure revenue model is not empty"""
        if not v or (isinstance(v, str) and not v.strip()):
            return "Unknown"
        return v


class NewsSection(BaseModel):
    news_items: List[NewsItem] = Field(..., min_items=1)
    
    @field_validator('news_items', mode='before')
    @classmethod
    def validate_news_items(cls, v):
        """Ensure news items list is never empty"""
        if not v or len(v) == 0:
            return [{"title": "Company News", "summary": None, "date": None}]
        return v


class ReferencesSection(BaseModel):
    references: List[Reference] = Field(..., min_items=1)
    
    @field_validator('references', mode='before')
    @classmethod
    def validate_references(cls, v):
        """Ensure references list is never empty"""
        if not v or len(v) == 0:
            return [{"source_name": "Research", "url": "https://example.com"}]
        return v


class StructuredCompanyReport(BaseModel):
    company_name: str
    overview: CompanyOverview
    industry: IndustryOverview
    financials: FinancialOverview
    news: NewsSection
    references: ReferencesSection
    
    @field_validator('company_name', mode='before')
    @classmethod
    def validate_company_name(cls, v):
        """Ensure company name is not empty"""
        if not v or (isinstance(v, str) and not v.strip()):
            return "Unknown Company"
        return v
      
    @classmethod
    def create_fallback(cls, company_name: str) -> "StructuredCompanyReport":
        """Create fallback report using Pydantic schema defaults"""
        return cls(
            company_name=company_name,
            overview={
                "business_description": "Information about the company",
                "core_products_and_services": ["Product/Service"],
                "leadership_team": [{"name": "Unknown", "role": "Leadership"}],
                "competitive_advantages": [{"point": "Company presence"}]
            },
            industry={
                "market_landscape": "Information not available",
                "competition": ["Competitor 1"]
            },
            financials={
                "revenue_model": "Unknown"
            },
            news={
                "news_items": [{"title": "Company News"}]
            },
            references={
                "references": [{"source_name": "Research", "url": "https://example.com"}]
            }
        )

    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "Vodafone",
                "overview": {
                    "business_description": "Global telecommunications provider",
                    "core_products_and_services": ["Mobile Services", "Broadband"],
                    "leadership_team": [
                        {"name": "Margherita Della Valle", "role": "CEO"}
                    ],
                    "target_market": "Consumers and businesses",
                    "competitive_advantages": [
                        {"point": "Global network reach"},
                        {"point": "Strong brand recognition"}
                    ],
                    "business_model": "Subscription-based services",
                    "funding_and_investment": "Public company"
                },
                "industry": {
                    "market_landscape": "Global telecommunications market",
                    "competition": ["China Mobile", "AT&T"],
                    "market_challenges": "Regulatory pressure and competition"
                },
                "financials": {
                    "revenue_model": "Subscriptions and enterprise services",
                    "revenue_2024": "40.5B",
                    "growth_rate": "2%",
                    "net_income_change": "-465.7%"
                },
                "news": {
                    "news_items": [
                        {"title": "Vodafone increases dividend", "date": "2025-01-22"}
                    ]
                },
                "references": {
                    "references": [
                        {"source_name": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Vodafone"}
                    ]
                }
            }
        }

class CompanyReportResponse(BaseModel):
    """Response model for company report generation"""
    company_name: str
    report: StructuredCompanyReport