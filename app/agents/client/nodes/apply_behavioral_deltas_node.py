from app.agents.client.schemas.states.behavioral_state import BehavioralState
from app.agents.client.schemas.states.client_graph_state import ClientGraphState
from app.domain.constants.tolerance_initial_values import TOLERANCE_INITIAL_VALUES


def create_apply_behavioral_deltas_node():
    def apply_behavioral_deltas(state: ClientGraphState) -> dict[str, BehavioralState]:
        trust_assessment = state.get("trust_assessment")
        tolerance_assessment = state.get("tolerance_assessment")
        if trust_assessment is None or tolerance_assessment is None:
            raise ValueError("Trust and tolerance assessments are required.")

        behavioral_state_before = state["behavioral_state"]
        maximum_tolerance = TOLERANCE_INITIAL_VALUES[state["persona"].tolerance]
        behavioral_state_after = BehavioralState(
            trust=min(
                5.0,
                max(1.0, behavioral_state_before.trust + trust_assessment.trust_delta),
            ),
            tolerance=min(
                maximum_tolerance,
                max(
                    0,
                    behavioral_state_before.tolerance
                    + tolerance_assessment.tolerance_delta,
                ),
            ),
        )
        return {"behavioral_state_after": behavioral_state_after}

    return apply_behavioral_deltas
