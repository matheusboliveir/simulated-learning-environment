import logging
from collections.abc import Awaitable, Generator
from contextlib import contextmanager
from time import perf_counter
from typing import TypeVar

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(logging.StreamHandler())
logger.propagate = False

T = TypeVar("T")


@contextmanager
def measure_duration(stage: str) -> Generator[None, None, None]:
    started_at = perf_counter()
    try:
        yield
    finally:
        logger.info(
            "stage_duration stage=%s duration_ms=%.2f",
            stage,
            (perf_counter() - started_at) * 1000,
        )


async def measure_awaitable(stage: str, awaitable: Awaitable[T]) -> T:
    with measure_duration(stage):
        return await awaitable
