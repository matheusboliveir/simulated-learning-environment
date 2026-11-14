import json

from pydantic import BaseModel

from app.agents.client.sub_agents.interaction_evaluator.schemas.identified_behavior import (
    IdentifiedBehavior,
)
from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)


def format_retrieved_messages(
    messages: list[SimulationMessage],
) -> str:
    formatted_messages = [
        f"[{msg.role}]: {msg.content} (Trust delta: {msg.trust_delta}, Tolerance delta: {msg.tolerance_delta})"
        for msg in messages
    ]

    return json.dumps(
        formatted_messages,
        ensure_ascii=False,
        indent=2,
    )


def format_untrusted_text(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def format_persona_snapshot(
    persona: PersonaSnapshotModel,
) -> str:
    data = {
        "name": persona.name,
        "position": persona.position,
        "knowledge": persona.knowledge,
        "personality": persona.personality,
        "communication_style": persona.communication_style,
        "tolerance": persona.tolerance.value,
        "background": persona.background,
        "pain_points": persona.pain_points,
        "biases": persona.biases,
    }

    return json.dumps(data, ensure_ascii=False, indent=2)


def format_identified_behaviors(behaviors: list[IdentifiedBehavior]) -> str:
    data = [
        {
            "behavior": item.behavior.value,
            "evidence": item.evidence,
            "confidence_relevant": item.confidence_relevant,
        }
        for item in behaviors
    ]

    return json.dumps(data, ensure_ascii=False, indent=2)


def format_schema(schema: BaseModel) -> str:
    data = schema.model_dump(mode="json", exclude_none=True)

    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    )
