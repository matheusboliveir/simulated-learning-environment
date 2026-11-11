
import json

from collections.abc import Sequence
from pydantic import BaseModel


def format_retrieved_messages(
    messages: Sequence[BaseModel],
) -> str:
    formatted_messages = [
        message.model_dump(mode="json", exclude_none=True)
        for message in messages
    ]

    return json.dumps(
        formatted_messages,
        ensure_ascii=False,
        indent=2,
    )


def format_untrusted_text(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)
