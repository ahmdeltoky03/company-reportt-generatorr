from crewai import Agent, Task
from langchain_cohere import ChatCohere


class AnalysisAgent:
    """Agent for analyzing company data and structuring it"""
    
    def __init__(self, llm: ChatCohere):
        self.llm = llm
    
    def create_agent(self) -> Agent:
        """Create and return analysis agent"""
        return Agent(
            role="Data Structure Expert",
            goal="Transform company research into organized, detailed structured information",
            backstory="Expert at organizing and structuring business information for professional reports.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_task(self, agent: Agent, research_findings: str) -> Task:
        """Create analysis task for structuring data"""
        return Task(
            description=f"""Organize and structure this research data into detailed categories:

{research_findings}

Create detailed information organized as follows:

**COMPANY OVERVIEW:**
- Business Description: [Detailed 2-3 sentence description]
- Products & Services: [List each product/service separately]
- Leadership Team: [List with name and role for each person]
- Target Market: [Who they serve]
- Competitive Advantages: [At least 3 specific advantages]
- Business Model: [How they make money]
- Funding & Investment: [Investment details]

**INDUSTRY ANALYSIS:**
- Market Landscape: [Industry description]
- Main Competitors: [List competitors]
- Market Challenges: [Challenges in the industry]

**FINANCIAL INFORMATION:**
- Revenue Model: [How revenue is generated]
- Revenue Figures: [Specific amounts and years]
- Growth Metrics: [Growth rates and changes]
- Key Metrics: [Important business metrics]

**RECENT NEWS:**
- News Items: [With titles, dates, and summaries]

**SOURCES & REFERENCES:**
- References: [Source names and URLs]

Be specific and detailed. Use exact figures and names from the research data.""",
            agent=agent,
            expected_output="Detailed structured information organized by category, ready for JSON schema mapping"
        )