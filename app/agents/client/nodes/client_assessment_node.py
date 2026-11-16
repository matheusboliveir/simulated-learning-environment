from typing import TypedDict

from langchain_core.language_models.chat_models import BaseChatModel

from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.agents.client.sub_agents.client_assessment.agent import (
    ClientAssessmentAgent,
)
from app.agents.client.sub_agents.client_assessment.schemas.client_assessment_input import (
    ClientAssessmentInput,
)
from app.agents.client.sub_agents.client_assessment.schemas.interaction_assessment_output import (
    InteractionAssessmentOutput,
)
from app.agents.client.sub_agents.client_assessment.schemas.tolerance_assessment_output import (
    ToleranceAssessmentOutput,
)
from app.agents.client.sub_agents.client_assessment.schemas.trust_assessment_output import (
    TrustAssessmentOutput,
)


class ClientAssessmentNodeOutput(TypedDict):
    interaction_assessment: InteractionAssessmentOutput
    trust_assessment: TrustAssessmentOutput
    tolerance_assessment: ToleranceAssessmentOutput


def create_client_assessment_node(llm: BaseChatModel):
    agent = ClientAssessmentAgent(llm)

    async def client_assessment(
        state: ClientGraphState,
    ) -> ClientAssessmentNodeOutput:
        assessment = await agent.evaluate(
            ClientAssessmentInput(
                business_context=state.get("business_context") or "no context",
                retrieved_messages=state.get("retrieved_messages") or [],
                student_message=state["student_message"],
                persona=state["persona"],
                behavioral_state=state["behavioral_state"],
            )
        )
        return {
            "interaction_assessment": assessment.interaction_assessment,
            "trust_assessment": assessment.trust_assessment,
            "tolerance_assessment": assessment.tolerance_assessment,
        }

    return client_assessment
