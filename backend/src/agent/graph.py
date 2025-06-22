from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from agent.generate_queries import generate_search_queries
from agent.continue_to_web_research import continue_to_web_research
from agent.web_research import web_research
from agent.reflection import reflect_on_search_results
from agent.evaluate_research import evaluate_research
from agent.finalize_answer import finalize_answer
from agent.state import OverallState

builder = StateGraph(OverallState)

builder.add_node("generate_query", generate_search_queries)
builder.add_node("web_research", web_research)
builder.add_node("reflection", reflect_on_search_results)
builder.add_node("finalize_answer", finalize_answer)


builder.add_edge(START, "generate_query")
builder.add_conditional_edges(
    "generate_query",
    continue_to_web_research,
    ["web_research"],
)

builder.add_edge("web_research", "reflection")

builder.add_conditional_edges(
    "reflection",
    evaluate_research,
    ["web_research", "finalize_answer"])

builder.add_edge("finalize_answer", END)

graph = builder.compile(name="pro-search-agent")