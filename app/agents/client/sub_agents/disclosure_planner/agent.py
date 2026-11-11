from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.agents.client.sub_agents.disclosure_planner.prompt import (
    DISCLOSURE_PLANNER_HUMAN_PROMPT,
    DISCLOSURE_PLANNER_SYSTEM_PROMPT,
)
from app.agents.client.sub_agents.disclosure_planner.schemas.disclosure_planner_input import (
    DisclosurePlannerInput,
)
from app.agents.client.sub_agents.disclosure_planner.schemas.disclosure_planner_output import (
    DisclosurePlannerOutput,
)
from app.utils.formatter import (
    format_persona_snapshot,
    format_retrieved_messages,
    format_schema,
    format_untrusted_text,
)


class DisclosurePlanner:
    def __init__(self, llm: BaseChatModel) -> None:
        self._llm = llm.with_structured_output(DisclosurePlannerOutput)

        self._prompt = ChatPromptTemplate.from_messages(
            [
                ("system", DISCLOSURE_PLANNER_SYSTEM_PROMPT),
                ("human", DISCLOSURE_PLANNER_HUMAN_PROMPT),
            ]
        )

        self._chain = self._prompt | self._llm

    async def evaluate(
        self,
        input: DisclosurePlannerInput,
    ) -> DisclosurePlannerOutput:

        result = await self._chain.ainvoke(
            {
                "business_context": format_untrusted_text(input.business_context),
                "retrieved_messages": format_retrieved_messages(
                    input.retrieved_messages
                ),
                "behavioral_state": format_schema(input.behavioral_state),
                "trust_assessment": format_schema(input.trust_assessment),
                "tolerance_assessment": format_schema(input.tolerance_assessment),
                "student_message": format_untrusted_text(input.student_message),
                "persona_snapshot": format_persona_snapshot(input.persona),
            }
        )

        output = DisclosurePlannerOutput.model_validate(result)

        return output
