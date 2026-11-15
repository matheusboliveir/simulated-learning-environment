from langchain.chat_models import BaseChatModel

from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.agents.client.sub_agents.trust_evaluator.agent import TrustEvaluator
from app.agents.client.sub_agents.trust_evaluator.schemas.trust_evaluator_input import TrustEvaluatorInput


def create_trust_evaluator_node(llm: BaseChatModel):
    
    subagent = TrustEvaluator(llm)
    
    def trust_evaluator(state: ClientGraphState):
        interaction_assessment = state.get("interaction_assessment")
        identified_behaviors = (
            interaction_assessment.identified_behaviors
            if interaction_assessment is not None
            else []
        )
        
        retrieved_messages = state.get("retrieved_messages")
        retrieved_messages = retrieved_messages if retrieved_messages is not None else []
        
        input = TrustEvaluatorInput(
            persona=state["persona"],
            current_trust=state["behavioral_state"].trust,
            student_message=state["student_message"],
            retrieved_messages=retrieved_messages,
            identified_behaviors=identified_behaviors,
        )
        result = subagent.evaluate(input)
        return { "trust_assessment": result } 
    
    return trust_evaluator