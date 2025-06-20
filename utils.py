from datetime import datetime
from typing import Any, Dict, List
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage


# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")

def get_research_topic(messages: List[AnyMessage]) -> str:
    """
    Get the research topic from the messages.
    """
    # check if request has a history and combine the messages into a single string
    if len(messages) == 1:
        research_topic = messages[-1].content
    else:
        research_topic = ""
        for message in messages:
            if isinstance(message, HumanMessage):
                research_topic += f"User: {message.content}\n"
            elif isinstance(message, AIMessage):
                research_topic += f"Assistant: {message.content}\n"
    return research_topic