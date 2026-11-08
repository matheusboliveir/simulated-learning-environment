import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.simulation.simulation import SimulationModel

ph = PasswordHasher()


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    @property
    def password(self):
        raise AttributeError("The password cannot be read directly in plain text.")

    @password.setter
    def password(self, plain_password: str):
        self.password_hash = ph.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        try:
            return ph.verify(self.password_hash, plain_password)
        except VerifyMismatchError:
            return False

    email: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    simulations: Mapped[list["SimulationModel"]] = relationship(back_populates="user")
