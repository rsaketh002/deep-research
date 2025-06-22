import asyncio
from tavily import AsyncTavilyClient
from langchain_openai import ChatOpenAI
from agent.state import OverallState, WebSearchState
from agent.prompts import web_researcher_prompt
from dotenv import load_dotenv
load_dotenv()

# Async fetch function
async def fetch_and_gather(search_queries):
    tavily_client = AsyncTavilyClient()
    response = await tavily_client.search(
        search_queries,
        search_depth="advanced",
        include_answer="advanced",
        max_results=5,
    )
    return response

def format_search_results(queries_with_results):
    formatted = ""
    q = queries_with_results
    formatted += f"🔍 Query: {q['query']}\n"
    for i, result in enumerate(q.get("results", []), 1):
        formatted += (
            f"{i}. Title: {result['title']}\n"
            f"   URL: {result['url']}\n"
            f"   Content: {result['content']}\n"
        )
    return formatted

# The web research function (now async)
async def web_research(state: WebSearchState) -> OverallState:
    search_results = await fetch_and_gather(state["search_query"])
    formatted_results = format_search_results(search_results)
    
    llm = ChatOpenAI(
        model="o4-mini-2025-04-16",  # Change to your available model or "o4-mini-2025-04-16" if enabled for your account
        temperature=1,
    )
    
    result = await llm.ainvoke(
        [
            {
                "role": "system",
                "content": web_researcher_prompt
            },
            {
                "role": "user",
                "content": f"Here are the search results: {formatted_results}"
            }
        ]
    )
    
    sources_gathered = []
    for res in search_results.get('results', []):
        if res['url'] not in sources_gathered:
            sources_gathered.append(res['url'])
                
    return {
        "web_research_result": [result.content],
        "sources_gathered": sources_gathered,
        "search_query": [state["search_query"]],
    }

# Example usage for testing
if __name__ == "__main__":
    async def main():
        state = {
            "search_query": [
                "Latest India geopolitical news and analysis June 2025"
            ]
        }
        result = await web_research(state)
        print(result)

    asyncio.run(main())
