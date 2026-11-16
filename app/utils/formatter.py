import json

from pydantic import BaseModel

from app.domain.schemas.simulation_message_schema import SimulationMessage
from app.infrastructure.database.models.simulation.persona_snapshot import (
    PersonaSnapshotModel,
)


def format_retrieved_messages(
    messages: list[SimulationMessage],
) -> str:
    formatted_messages = [
        f"[Sequence: {msg.sequence}] [{msg.role}]: {msg.content} (Trust delta: {msg.trust_delta}, Tolerance delta: {msg.tolerance_delta})"
        for msg in messages
    ]

    return json.dumps(
        formatted_messages,
        ensure_ascii=False,
        indent=2,
    )


def format_untrusted_text(value: str | None) -> str:
    if not value:
        return ""
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


def format_schema(schema: BaseModel | None) -> str:
    if not schema:
        return ""
    data = schema.model_dump(mode="json", exclude_none=True)

    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    )
