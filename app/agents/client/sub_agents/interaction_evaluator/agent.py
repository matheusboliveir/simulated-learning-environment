
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.agents.client.sub_agents.interaction_evaluator.prompt import INTERACTION_EVALUATOR_HUMAN_PROMPT, INTERACTION_EVALUATOR_SYSTEM_PROMPT
from app.agents.client.sub_agents.interaction_evaluator.schemas.interaction_evaluator_input import InteractionEvaluatorInput
from app.agents.client.sub_agents.interaction_evaluator.schemas.interaction_evaluator_output import InteractionEvaluatorOutput
from app.agents.client.sub_agents.interaction_evaluator.utils.formatter import (format_untrusted_text, format_retrieved_messages)



class InteractionEvaluator:

    def __init__(self, llm: BaseChatModel):
        self._prompt = ChatPromptTemplate.from_messages(
            [
                ("system", INTERACTION_EVALUATOR_SYSTEM_PROMPT),
                ("human", INTERACTION_EVALUATOR_HUMAN_PROMPT),
            ]
        )

        self._chain = (
            self._prompt
            | llm.with_structured_output(InteractionEvaluatorOutput)
        )

    async def evaluate(
        self,
        evaluator_input: InteractionEvaluatorInput,
    ) -> InteractionEvaluatorOutput:

        payload = {
            "business_context": format_untrusted_text(
                evaluator_input.business_context
            ),
            "retrieved_messages": format_retrieved_messages(
                evaluator_input.retrieved_messages
            ),
            "student_message": format_untrusted_text(
                evaluator_input.student_message
            ),
        }

        result = await self._chain.ainvoke(payload)

        return InteractionEvaluatorOutput.model_validate(result)
