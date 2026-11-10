from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid

from langchain_protocol import MessageRole
from sqlalchemy import DateTime, Float, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
	from app.infrastructure.database.models.simulation.simulation import SimulationModel


class SimulationMessageModel(Base):
    __tablename__ = "simulation_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

	# Simulação da mensagem
    simulation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("simulations.id"), nullable=False
    )
    simulation: Mapped["SimulationModel"] = relationship(back_populates="messages")

	# Quem enviou a mensagem
    role: Mapped[MessageRole] = mapped_column(String(20), nullable=False)
    
    # Conteudo da mensagem
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Delta de reação calculados
    tolerance_delta: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    trust_delta: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )