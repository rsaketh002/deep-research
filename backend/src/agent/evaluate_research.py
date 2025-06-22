from agent.state import OverallState, ReflectionState
from langgraph.types import Send

def evaluate_research(
    state: ReflectionState,
) -> OverallState:
    max_research_loops = (
        state.get("max_research_loops")
        if state.get("max_research_loops") is not None
        else 5
    )

    # Initialize queries_sent if not present
    if "queries_sent" not in state:
        state["queries_sent"] = set()

    # Filter follow-up queries to only new ones
    new_queries = [
        q for q in state["follow_up_queries"] if q not in state["queries_sent"]
    ]

    # Update queries_sent with new queries
    state["queries_sent"].update(new_queries)

    if state["is_sufficient"] or state["research_loop_count"] >= max_research_loops:
        return "finalize_answer"
    else:
        return [
            Send(
                "web_research",
                {
                    "search_query": follow_up_query,
                    "id": state["number_of_ran_queries"] + int(idx),
                },
            )
            for idx, follow_up_query in enumerate(new_queries)
        ]
