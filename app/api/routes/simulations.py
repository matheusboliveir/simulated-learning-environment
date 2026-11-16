from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.simulations import (
    get_create_simulation,
    get_send_message,
)
from app.api.schemas.simulations.create_simulation_request import (
    CreateSimulationRequest,
)
from app.api.schemas.simulations.send_message_request import SendMessageRequest
from app.api.schemas.simulations.simulation_response import SimulationResponse
from app.application.simulations.create_simulation import CreateSimulation
from app.application.simulations.send_message import SendMessage

router = APIRouter(prefix="/simulations", tags=["Simulations"])


@router.post(
    "",
    response_model=SimulationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_simulation(
    body: CreateSimulationRequest,
    use_case: Annotated[CreateSimulation, Depends(get_create_simulation)],
) -> SimulationResponse:
    try:
        simulation = await use_case.execute(
            user_id=body.user_id,
            case_snapshot_id=body.case_snapshot_id,
        )
        return SimulationResponse.model_validate(simulation)
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post("/{simulation_id}/messages")
async def send_message(
    simulation_id: UUID,
    body: SendMessageRequest,
    use_case: Annotated[SendMessage, Depends(get_send_message)],
):
    return await use_case.execute(
        simulation_id=simulation_id,
        student_message=body.content,
    )