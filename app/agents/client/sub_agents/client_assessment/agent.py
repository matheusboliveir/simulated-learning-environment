from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.agents.client.sub_agents.client_assessment.prompt import (
    CLIENT_ASSESSMENT_HUMAN_PROMPT,
    CLIENT_ASSESSMENT_SYSTEM_PROMPT,
)
from app.agents.client.sub_agents.client_assessment.schemas.client_assessment_input import (
    ClientAssessmentInput,
)
from app.agents.client.sub_agents.client_assessment.schemas.client_assessment_output import (
    ClientAssessmentOutput,
)
from app.agents.client.sub_agents.client_assessment.utils.formatter import (
    format_tolerance_ranges,
)
from app.domain.constants.tolerance_initial_values import TOLERANCE_INITIAL_VALUES
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
        self._chain = prompt | llm.with_structured_output(ClientAssessmentOutput)

    async def evaluate(
        self,
        input: ClientAssessmentInput,
    ) -> ClientAssessmentOutput:
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
                    "maximum_tolerance": TOLERANCE_INITIAL_VALUES[
                        input.persona.tolerance
                    ],
                    "tolerance_ranges": format_tolerance_ranges(),
                }
            ),
        )
        return ClientAssessmentOutput.model_validate(result)
