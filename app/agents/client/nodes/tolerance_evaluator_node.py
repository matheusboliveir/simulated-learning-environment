from langchain.chat_models import BaseChatModel

from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.agents.client.sub_agents.tolerance_evaluator.agent import ToleranceEvaluator
from app.agents.client.sub_agents.tolerance_evaluator.schemas.tolerance_evaluator_input import ToleranceEvaluatorInput


def create_tolerance_evaluator_node(llm: BaseChatModel):
    
    subagent = ToleranceEvaluator(llm)
    
    def tolerance_evaluator(state: ClientGraphState):
        interaction_assessment = state.get("interaction_assessment")
        identified_behaviors = (
            interaction_assessment.identified_behaviors
            if interaction_assessment is not None
            else []
        )
        input = ToleranceEvaluatorInput(
            persona=state["persona"],
            current_tolerance=state["behavioral_state"].tolerance,
            identified_behaviors=identified_behaviors,
        )
        result = subagent.evaluate(input)
        return { "tolerance_assessment": result } 
    
    return tolerance_evaluator