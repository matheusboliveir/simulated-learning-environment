from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.agents.client.sub_agents.trust_evaluator.prompt import (
    TRUST_EVALUATOR_HUMAN_PROMPT,
    TRUST_EVALUATOR_SYSTEM_PROMPT,
)
from app.agents.client.sub_agents.trust_evaluator.schemas.trust_evaluator_input import (
    TrustEvaluatorInput,
)
from app.agents.client.sub_agents.trust_evaluator.schemas.trust_evaluator_output import (
    TrustEvaluatorOutput,
)
from app.utils.formatter import (
    format_identified_behaviors,
    format_persona_snapshot,
    format_retrieved_messages,
    format_untrusted_text,
)


class TrustEvaluator:
    def __init__(self, llm: BaseChatModel) -> None:
        self._llm = llm.with_structured_output(TrustEvaluatorOutput)

        self._prompt = ChatPromptTemplate.from_messages(
            [
                ("system", TRUST_EVALUATOR_SYSTEM_PROMPT),
                ("human", TRUST_EVALUATOR_HUMAN_PROMPT),
            ]
        )

        self._chain = self._prompt | self._llm

    async def evaluate(
        self,
        input: TrustEvaluatorInput,
    ) -> TrustEvaluatorOutput:

        if not input.identified_behaviors or len(input.identified_behaviors) == 0:
            return TrustEvaluatorOutput(
                trust_delta=0,
                reason="No identified behaviors were provided.",
                evaluated_behaviors=[],
            )

        if input.current_trust > 5:
            return TrustEvaluatorOutput(
                trust_delta=0,
                reason="Current trust exceeds the persona's maximum trust.",
                evaluated_behaviors=[],
            )

        result = await self._chain.ainvoke(
            {
                "persona_snapshot": format_persona_snapshot(input.persona_snapshot),
                "identified_behaviors": format_identified_behaviors(
                    input.identified_behaviors
                ),
                "retrieved_messages": format_retrieved_messages(
                    input.retrieved_messages
                ),
                "student_message": format_untrusted_text(input.student_message),
                "current_trust": input.current_trust,
            }
        )

        output = TrustEvaluatorOutput.model_validate(result)

        return output
