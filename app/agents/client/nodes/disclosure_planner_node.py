from langchain.chat_models import BaseChatModel

from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.agents.client.sub_agents.disclosure_planner.agent import DisclosurePlanner
from app.agents.client.sub_agents.disclosure_planner.schemas.disclosure_planner_input import (
    DisclosurePlannerInput,
)


def create_disclosure_planner_node(llm: BaseChatModel):

    subagent = DisclosurePlanner(llm)

    async def disclosure_planner(state: ClientGraphState):
        business_context = state.get("business_context")
        business_context = (
            business_context if business_context is not None else "no context"
        )

        retrieved_messages = state.get("retrieved_messages")
        retrieved_messages = (
            retrieved_messages if retrieved_messages is not None else []
        )

        tolerance_assessment = state.get("tolerance_assessment")

        trust_assessment = state.get("trust_assessment")

        if not tolerance_assessment or not trust_assessment:
            raise ValueError("no assessments found")
        behavioral_state_after = state.get("behavioral_state_after")
        if behavioral_state_after is None:
            raise ValueError("Post-interaction behavioral state is required.")

        input = DisclosurePlannerInput(
            retrieved_messages=retrieved_messages,
            business_context=business_context,
            persona=state["persona"],
            student_message=state["student_message"],
            behavioral_state_before=state["behavioral_state"],
            behavioral_state_after=behavioral_state_after,
            tolerance_assessment=tolerance_assessment,
            trust_assessment=trust_assessment,
        )
        result = await subagent.evaluate(input)
        return {"disclosure_plan": result}

    return disclosure_planner
