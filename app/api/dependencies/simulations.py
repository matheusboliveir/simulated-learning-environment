from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.client.agent import ClientAgent
from app.api.dependencies.case_snapshots import get_case_snapshot_repository
from app.api.dependencies.client_agent import get_client_agent
from app.api.dependencies.persona_snapshots import (
    get_persona_snapshot_repository,
)
from app.api.dependencies.users import get_user_repository
from app.application.simulations.create_simulation import CreateSimulation
from app.application.simulations.send_message import SendMessage
from app.infrastructure.database.connection import get_db
from app.infrastructure.database.repositories.case_snapshot_repository import (
    CaseSnapshotRepository,
)
from app.infrastructure.database.repositories.persona_snapshot_repository import (
    PersonaSnapshotRepository,
)
from app.infrastructure.database.repositories.simulation_repository import (
    SimulationRepository,
)
from app.infrastructure.database.repositories.user_repository import UserRepository


def get_simulation_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> SimulationRepository:
    return SimulationRepository(session)


def get_create_simulation(
    simulation_repository: Annotated[
        SimulationRepository,
        Depends(get_simulation_repository),
    ],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    case_snapshot_repository: Annotated[
        CaseSnapshotRepository,
        Depends(get_case_snapshot_repository),
    ],
    persona_snapshot_repository: Annotated[
        PersonaSnapshotRepository,
        Depends(get_persona_snapshot_repository),
    ],
) -> CreateSimulation:
    return CreateSimulation(
        simulation_repository=simulation_repository,
        user_repository=user_repository,
        case_snapshot_repository=case_snapshot_repository,
        persona_snapshot_repository=persona_snapshot_repository,
    )


def get_send_message(
    simulation_repository: Annotated[
        SimulationRepository,
        Depends(get_simulation_repository),
    ],
    client_agent: Annotated[ClientAgent, Depends(get_client_agent)],
) -> SendMessage:
    return SendMessage(
        simulation_repository=simulation_repository,
        client_agent=client_agent,
    )