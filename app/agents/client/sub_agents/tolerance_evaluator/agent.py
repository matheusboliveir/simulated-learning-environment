from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.agents.client.sub_agents.tolerance_evaluator.prompt import (
    TOLERANCE_EVALUATOR_HUMAN_PROMPT,
    TOLERANCE_EVALUATOR_SYSTEM_PROMPT,
)
from app.agents.client.sub_agents.tolerance_evaluator.schemas.tolerance_evaluator_input import (
    ToleranceEvaluatorInput,
)
from app.agents.client.sub_agents.tolerance_evaluator.schemas.tolerance_evaluator_output import (
    ToleranceEvaluatorOutput,
)
from app.agents.client.sub_agents.tolerance_evaluator.utils.formatter import (
    format_tolerance_initial_values,
    format_tolerance_ranges,
)
from app.domain.constants.tolerance_initial_values import TOLERANCE_INITIAL_VALUES
from app.utils.formatter import format_identified_behaviors, format_persona_snapshot


class ToleranceEvaluator:
    def __init__(self, llm: BaseChatModel) -> None:
        self._llm = llm.with_structured_output(ToleranceEvaluatorOutput)

        self._prompt = ChatPromptTemplate.from_messages(
            [
                ("system", TOLERANCE_EVALUATOR_SYSTEM_PROMPT),
                ("human", TOLERANCE_EVALUATOR_HUMAN_PROMPT),
            ]
        )

        self._chain = self._prompt | self._llm

    async def evaluate(
        self,
        input: ToleranceEvaluatorInput,
    ) -> ToleranceEvaluatorOutput:

        if not input.identified_behaviors or len(input.identified_behaviors) == 0:
            return ToleranceEvaluatorOutput(
                tolerance_delta=0,
                reason="No identified behaviors were provided.",
                evaluated_behaviors=[],
            )

        maximum_tolerance = TOLERANCE_INITIAL_VALUES[input.persona_snapshot.tolerance]

        if input.current_tolerance > maximum_tolerance:
            return ToleranceEvaluatorOutput(
                tolerance_delta=0,
                reason="Current tolerance exceeds the persona's maximum tolerance.",
                evaluated_behaviors=[],
            )

        result = await self._chain.ainvoke(
            {
                "persona_snapshot": format_persona_snapshot(input.persona_snapshot),
                "current_tolerance": input.current_tolerance,
                "maximum_tolerance": maximum_tolerance,
                "identified_behaviors": format_identified_behaviors(
                    input.identified_behaviors
                ),
                "tolerance_ranges": format_tolerance_ranges(),
                "tolerance_initial_values": format_tolerance_initial_values(),
            }
        )

        output = ToleranceEvaluatorOutput.model_validate(result)

        return output
