from datetime import datetime
from typing import TYPE_CHECKING, List
import uuid

from sqlalchemy import ARRAY, DateTime, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums.tolerance_preset import TolerancePreset
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.simulation.case_snapshot import CaseSnapshotModel


class PersonaSnapshotModel(Base):
    __tablename__ = "persona_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Dados
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    position: Mapped[str] = mapped_column(String(50), nullable=False)
    knowledge: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)

    # Comportamento e tom
    personality: Mapped[str] = mapped_column(String(255), nullable=False)
    communication_style: Mapped[str] = mapped_column(String(100), nullable=False)
    tolerance: Mapped[TolerancePreset] = mapped_column(
        nullable=False,
        default=TolerancePreset.PROFESSIONAL,
    )
    
    # Interesses
    background: Mapped[str] = mapped_column(Text, nullable=False)
    pain_points: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    biases: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    
    # Controle de criação
    case_snapshots: Mapped[List["CaseSnapshotModel"]] = relationship(
        back_populates="persona_snapshot"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )