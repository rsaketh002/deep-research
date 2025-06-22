from agent.state import OverallState, ReflectionState
from agent.schemas import Reflection
from agent.utils import get_current_date, get_research_topic
from agent.prompts import reflection_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def reflect_on_search_results(state: OverallState) -> ReflectionState:
    state["research_loop_count"] = state.get("research_loop_count", 0) + 1

    llm = ChatOpenAI(
        model="o4-mini-2025-04-16",
        temperature=1.0,
    )

    structured_llm = llm.with_structured_output(Reflection)

    formatted_prompt = reflection_prompt.format(
        current_date = get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        summaries="\n\n---\n\n".join(state["web_research_result"]),
    )

    response = structured_llm.invoke(formatted_prompt)

    return {
        "is_sufficient": response.is_sufficient,
        "knowledge_gap": response.knowledge_gap,
        "follow_up_queries": response.follow_up_queries,
        "research_loop_count": state["research_loop_count"],
        "number_of_ran_queries": len(state["search_query"]),
    }
