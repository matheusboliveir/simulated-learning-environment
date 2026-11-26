from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.agents.client.sub_agents.client_assessment.prompt import (
    CLIENT_ASSESSMENT_HUMAN_PROMPT,
    CLIENT_ASSESSMENT_SYSTEM_PROMPT,
)
from app.agents.client.sub_agents.client_assessment.schemas.client_assessment_input import (
    ClientAssessmentInput,
)
from app.agents.client.sub_agents.client_assessment.schemas.client_assessment_llm_output import (
    ClientAssessmentLLMOutput,
)
from app.agents.client.sub_agents.client_assessment.schemas.client_assessment_output import (
    ClientAssessmentOutput,
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
from app.agents.client.sub_agents.client_assessment.utils.formatter import (
    format_tolerance_ranges,
    format_trust_ranges,
)
from app.domain.constants.tolerance_initial_values import TOLERANCE_INITIAL_VALUES
from app.domain.services.behavioral_deltas import calculate_behavioral_deltas
from app.utils.formatter import (
    format_persona_snapshot,
    format_retrieved_messages,
    format_schema,
    format_untrusted_text,
)
from app.utils.timing import measure_awaitable


class ClientAssessmentAgent:
    def __init__(self, llm: BaseChatModel) -> None:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", CLIENT_ASSESSMENT_SYSTEM_PROMPT),
                ("human", CLIENT_ASSESSMENT_HUMAN_PROMPT),
            ]
        )
        self._chain = prompt | llm.with_structured_output(ClientAssessmentLLMOutput)

    async def evaluate(
        self,
        input: ClientAssessmentInput,
    ) -> ClientAssessmentOutput:
        maximum_tolerance = TOLERANCE_INITIAL_VALUES[input.persona.tolerance]
        result = await measure_awaitable(
            "client.client_assessment.llm",
            self._chain.ainvoke(
                {
                    "persona_snapshot": format_persona_snapshot(input.persona),
                    "business_context": format_untrusted_text(input.business_context),
                    "retrieved_messages": format_retrieved_messages(
                        input.retrieved_messages
                    ),
                    "student_message": format_untrusted_text(input.student_message),
                    "behavioral_state": format_schema(input.behavioral_state),
                    "maximum_tolerance": maximum_tolerance,
                    "tolerance_ranges": format_tolerance_ranges(),
                    "trust_ranges": format_trust_ranges(),
                }
            ),
        )
        llm_output = ClientAssessmentLLMOutput.model_validate(result)
        return self._build_output(llm_output, input, maximum_tolerance)

    @staticmethod
    def _build_output(
        llm_output: ClientAssessmentLLMOutput,
        input: ClientAssessmentInput,
        maximum_tolerance: float,
    ) -> ClientAssessmentOutput:
        # Mensagem não compreendida: nenhum comportamento é avaliado e
        # confiança e tolerância não mudam (regra garantida pelo código).
        if not llm_output.message_understood:
            reason = "The client did not understand the message; no change."
            return ClientAssessmentOutput(
                interaction_assessment=InteractionAssessmentOutput(
                    identified_behaviors=[]
                ),
                trust_assessment=TrustAssessmentOutput(
                    trust_delta=0.0,
                    reason=reason,
                    evaluated_criteria=[],
                ),
                tolerance_assessment=ToleranceAssessmentOutput(
                    tolerance_delta=0,
                    reason=reason,
                    evaluated_behaviors=[],
                ),
            )

        behaviors = llm_output.interaction_assessment.identified_behaviors
        deltas = calculate_behavioral_deltas(
            behaviors=[(item.behavior, item.intensity) for item in behaviors],
            current_tolerance=input.behavioral_state.tolerance,
            maximum_tolerance=maximum_tolerance,
        )
        return ClientAssessmentOutput(
            interaction_assessment=llm_output.interaction_assessment,
            trust_assessment=TrustAssessmentOutput(
                trust_delta=deltas.trust_delta,
                reason=llm_output.trust_reason,
                evaluated_criteria=llm_output.trust_criteria,
            ),
            tolerance_assessment=ToleranceAssessmentOutput(
                tolerance_delta=deltas.tolerance_delta,
                reason=llm_output.tolerance_reason,
                evaluated_behaviors=sorted(
                    {item.behavior for item in behaviors},
                    key=lambda behavior: behavior.value,
                ),
            ),
        )
