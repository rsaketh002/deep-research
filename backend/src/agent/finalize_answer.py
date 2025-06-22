from agent.state import OverallState
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from agent.utils import get_current_date, get_research_topic
from agent.prompts import answer_prompt
from dotenv import load_dotenv
load_dotenv()


def finalize_answer(state: OverallState):
    """LangGraph node that finalizes the research summary.

    Prepares the final output by deduplicating and formatting sources, then
    combining them with the running summary to create a well-structured
    research report with proper citations.

    Args:
        state: Current graph state containing the running summary and sources gathered

    Returns:
        Dictionary with state update, including running_summary key containing the formatted final summary with sources
    """

    # Format the prompt
    current_date = get_current_date()
    formatted_prompt = answer_prompt.format(
        current_date=current_date,
        research_topic=get_research_topic(state["messages"]),
        summaries="\n---\n\n".join(state["web_research_result"]),
    )

    # init Reasoning Model, default to Gemini 2.5 Flash
    llm = ChatOpenAI(
        model="o4-mini-2025-04-16",  # Change to your available model or "o4-mini-2025-04-16" if enabled for your account
        temperature=1,
    )
    result = llm.invoke(formatted_prompt)

    return {
        "messages": [AIMessage(content=result.content)],
    }