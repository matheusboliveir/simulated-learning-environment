import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums.simulation_status import SimulationStatus
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.simulation.case_snapshot import (
        CaseSnapshotModel,
    )
    from app.infrastructure.database.models.simulation.simulation_message import (
        SimulationMessageModel,
    )
    from app.infrastructure.database.models.user.user import UserModel


class SimulationModel(Base):
    __tablename__ = "simulations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Usuário
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    user: Mapped["UserModel"] = relationship(back_populates="simulations")

    # Snapshot do caso usado
    case_snapshot_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("case_snapshots.id"), nullable=False
    )
    case_snapshot: Mapped["CaseSnapshotModel"] = relationship(
        back_populates="simulations"
    )

    # Hitórico de mensagens
    messages: Mapped[list["SimulationMessageModel"]] = relationship(
        back_populates="simulation",
        cascade="all, delete-orphan",
        order_by="SimulationMessageModel.created_at",
    )

    # Estados dinâmincos
    current_tolerance: Mapped[float] = mapped_column(Float, nullable=False)
    current_trust: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    status: Mapped[SimulationStatus] = mapped_column(
        nullable=False,
        default=SimulationStatus.CREATED,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
