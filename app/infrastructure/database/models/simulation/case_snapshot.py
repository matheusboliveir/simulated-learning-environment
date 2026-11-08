import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.simulation.persona_snapshot import (
        PersonaSnapshotModel,
    )
    from app.infrastructure.database.models.user.user import UserModel


class CaseSnapshotModel(Base):
    __tablename__ = "case_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cases.id"), nullable=False)

    case: Mapped["UserModel"] = relationship(back_populates="snapshots")

    persona_snapshot_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("persona_snapshots.id"), nullable=False
    )

    persona_snapshot: Mapped["PersonaSnapshotModel"] = relationship(
        back_populates="case_snapshots"
    )

    context_snapshot_id: Mapped[int] = mapped_column(nullable=False)

    version: Mapped[int] = mapped_column(nullable=False, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
