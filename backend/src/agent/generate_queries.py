from langchain_core.messages import HumanMessage

from agent.state import OverallState, QueryGenerationState
from agent.schemas import SearchQueryList
from agent.utils import get_current_date, get_research_topic
from agent.prompts import generate_queries_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def generate_search_queries(state: OverallState) -> QueryGenerationState:
    """
    Generates search queries for the given topic using the LLM.

    Args:
        state (OverallState): The current state of the application.

    Returns:
        OverallState: Updated state with generated search queries.
    """

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=1,
    )

    structured_llm = llm.with_structured_output(SearchQueryList) # type 
    current_date = get_current_date()
    research_topic = get_research_topic(state["messages"])
    num_queries = state["initial_search_query_count"]

    formatted_prompt = generate_queries_prompt.format(
        topic=research_topic,
        current_date=current_date,
        num_queries=num_queries
    )

    response = structured_llm.invoke(
        formatted_prompt
    )

    return {"search_query": response.query}
