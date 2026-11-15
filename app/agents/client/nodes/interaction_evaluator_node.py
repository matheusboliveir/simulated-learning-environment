from langchain_core.language_models import BaseChatModel

from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.agents.client.sub_agents.interaction_evaluator.agent import InteractionEvaluator
from app.agents.client.sub_agents.interaction_evaluator.schemas.interaction_evaluator_input import InteractionEvaluatorInput
from app.agents.client.sub_agents.interaction_evaluator.schemas.interaction_evaluator_output import InteractionEvaluatorOutput


def create_interaction_evaluator_node(
    llm: BaseChatModel,
):
    
    subagent = InteractionEvaluator(llm)

    async def interaction_evaluator(
        state: ClientGraphState,
    ) -> dict[str,InteractionEvaluatorOutput]:
        business_context = state.get("business_context")
        business_context = business_context if business_context is not None else "no context"
        retrieved_messages = state.get("retrieved_messages")
        retrieved_messages = retrieved_messages if retrieved_messages is not None else []
        
        input = InteractionEvaluatorInput(
            business_context=business_context,
            retrieved_messages=retrieved_messages,
            student_message=state["student_message"],
        )
        result = await subagent.evaluate(input)
        
        return { "interaction_assessment": result }
        
    return interaction_evaluator