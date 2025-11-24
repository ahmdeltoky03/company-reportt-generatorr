from tavily import TavilyClient
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class TavilySearchService:
    """Service for searching company information using Tavily API"""
    
    def __init__(self, tavily_api_key: str):
        """
        Initialize Tavily search service
        
        Args:
            tavily_api_key: Tavily API key
        """
        if not tavily_api_key or tavily_api_key.strip() == "":
            raise ValueError("Tavily API key is required")
        self.client = TavilyClient(api_key=tavily_api_key)
    
    def _execute_search(self, query: str) -> Dict[str, Any]:
        """Execute a single search query against Tavily API"""
        try:
            results = self.client.search(
                query=query,
                max_results=5,
                include_answer=True
            )
            print(f"[SEARCH] Query: '{query}' - Found results")
            return results
        except Exception as e:
            print(f"[WARNING] Search query failed for '{query}': {str(e)}")
            return None
    
    def search_company(self, company_name: str, company_link: Optional[str] = None) -> List[Dict[str, Any]]:
        """Run multiple parallel searches to gather comprehensive company data with optimized query count"""
        queries = [
            f"{company_name} company overview products services leadership",
            f"{company_name} revenue financials news 2024 2025",
        ]
        
        all_results = []
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {executor.submit(self._execute_search, query): query for query in queries}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    all_results.append(result)
        
        print(f"[INFO] Completed {len(all_results)} searches in parallel")
        return all_results
    
    def get_company_details(self, company_name: str, company_link: Optional[str] = None) -> Dict[str, Any]:
        """Extract and aggregate company information from all search results into structured format"""
        try:
            search_results = self.search_company(company_name, company_link)
            
            raw_content_parts = []
            sources_list = []
            
            for search_result in search_results:
                if isinstance(search_result, dict):
                    answer = search_result.get("answer", "")
                    if answer:
                        raw_content_parts.append(f"\n[ANSWER SECTION]\n{answer}\n")
                    
                    results = search_result.get("results", [])
                    if results:
                        for result in results:
                            if isinstance(result, dict):
                                title = result.get("title", "")
                                content = result.get("content", "")
                                url = result.get("url", "")
                                
                                if title or content:
                                    raw_content_parts.append(f"\n[SOURCE: {url}]\n")
                                    if title:
                                        raw_content_parts.append(f"Title: {title}\n")
                                    if content:
                                        raw_content_parts.append(f"{content}\n")
                                    
                                    if url and title:
                                        sources_list.append({
                                            "source_name": title[:50],
                                            "url": url
                                        })
            
            raw_content = "\n".join(raw_content_parts)
            
            if not raw_content.strip():
                raw_content = f"Information about {company_name} - No specific data found"
            
            return {
                "company_name": company_name,
                "search_results": search_results,
                "raw_content": raw_content,
                "sources": sources_list[:10]
            }
            
        except Exception as e:
            print(f"[ERROR] Error in get_company_details: {str(e)}")
            return {
                "company_name": company_name,
                "search_results": None,
                "raw_content": f"Information about {company_name}",
                "sources": []
            }