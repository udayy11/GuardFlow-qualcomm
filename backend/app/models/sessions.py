from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class Session(Base):
    """Session model representing user or system interaction sessions.
    
    Attributes:
        id: Primary key UUID
        started_at: When the session began
        ended_at: When the session concluded
        status: Current state of the session (active/terminated)
        current_risk_score: Numeric risk assessment
        current_risk_level: Categorized risk (low/medium/high)
    """

    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
        server_default=text("gen_random_uuid()"),
    )
    started_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    ended_at: Mapped[datetime | None]
    status: Mapped[str]  # Could use Enum in production
    current_risk_score: Mapped[float]
    current_risk_level: Mapped[str]

    def __repr__(self):
        return f"<Session {self.id} ({self.status})>"