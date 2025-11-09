from duckduckgo_search import DDGS
import time

def search_web(query, max_results=5):
    """
    Search the web using DuckDuckGo
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results
        
    Returns:
        list: List of search results with title, snippet, and link
    """
    try:
        print(f"🔍 Searching web for: {query}")
        
        with DDGS() as ddgs:
            results = []
            
            for result in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("body", ""),
                    "link": result.get("href", "")
                })
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
            
            print(f"✅ Found {len(results)} search results")
            return results
            
    except Exception as e:
        print(f"❌ Error searching web: {e}")
        return []

def format_search_results(results):
    """
    Format search results for LLM context
    
    Args:
        results (list): List of search result dictionaries
        
    Returns:
        str: Formatted search results
    """
    if not results:
        return "No search results found."
    
    formatted = "=== Web Search Results ===\n\n"
    
    for i, result in enumerate(results, 1):
        formatted += f"{i}. {result['title']}\n"
        formatted += f"   {result['snippet']}\n"
        formatted += f"   Source: {result['link']}\n\n"
    
    return formatted

def search_esg_news(query_terms="ESG regulations 2025", max_results=3):
    """
    Search for ESG-related news and updates
    
    Args:
        query_terms (str): Specific ESG query
        max_results (int): Number of results
        
    Returns:
        list: Search results
    """
    return search_web(query_terms, max_results)

def search_company_esg(company_name, max_results=3):
    """
    Search for company-specific ESG information
    
    Args:
        company_name (str): Name of company
        max_results (int): Number of results
        
    Returns:
        list: Search results
    """
    query = f"{company_name} ESG report sustainability 2024 2025"
    return search_web(query, max_results)