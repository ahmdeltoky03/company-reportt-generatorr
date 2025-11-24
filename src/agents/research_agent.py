from crewai import Agent, Task
from langchain_cohere import ChatCohere


class ResearchAgent:
    def __init__(self, llm: ChatCohere):
        """initialize research agent"""
        self.llm = llm
    
    def create_agent(self) -> Agent:
        """function to create search agent"""
        return Agent(
            role="Company Research Analyst",
            goal="Extract and organize ALL specific information about companies from research data",
            backstory="An expert analyst specializing in company research. You extract specific details from documents and organize them precisely.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_task(self, agent: Agent, company_data: str) -> Task:
        """Company Research Task"""
        task = Task(
            description=f"""Extract ALL specific information from this company data:

{company_data}

Extract EXACTLY these details:

1. BUSINESS DESCRIPTION: Clear description of what the company does (2-3 sentences)

2. PRODUCTS & SERVICES: List all specific products and services mentioned
   - Look for: mobile services, fixed services, broadband, cloud, IoT, payment services, etc.

3. LEADERSHIP TEAM: Extract names and titles of all executives mentioned
   - Format: "John Smith" - "CEO" or "Jane Doe" - "CFO"

4. TARGET MARKET: Who the company serves (consumers, businesses, enterprises, etc.)

5. COMPETITIVE ADVANTAGES: List specific strengths and differentiators
   - Examples: "Leader in 5G", "Largest network", "IoT solutions", etc.

6. BUSINESS MODEL: How the company makes money (subscriptions, usage charges, contracts, etc.)

7. FUNDING: Investment and funding information

8. MARKET LANDSCAPE: Description of the industry/market

9. COMPETITORS: Name specific competitors

10. MARKET CHALLENGES: What challenges exist in the market

11. FINANCIAL INFO: Revenue figures, growth rates, metrics
    - Extract: Revenue amounts, growth percentages, key financial metrics

12. NEWS: Recent news and announcements with dates

13. REFERENCES: Source names and URLs

Organize all findings clearly and factually based on the provided data.""",
            agent=agent,
            expected_output="Well-organized research findings with all specific company information extracted from the data"
        )
        return task