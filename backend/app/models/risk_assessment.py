from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class RiskAssessment(Base):
    """Risk assessment model for tracking security evaluations.
    
    Attributes:
        id: Primary key UUID
        session_id: Associated session (FK)
        score: Numeric risk valuation (0-100)
        level: Risk category (low/medium/high/critical)
        confidence: Scoring certainty percentage (0-100)
        triggered_rules: JSON array of rule IDs that fired
        requires_physical_confirmation: Whether human approval needed
        created_at: Assessment timestamp
    """

    __tablename__ = "risk_assessments"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
        server_default=text("gen_random_uuid()"),
    )
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.id"))
    score: Mapped[float]
    level: Mapped[str]
    confidence: Mapped[float]
    triggered_rules: Mapped[list[str]] = mapped_column(JSON)
    requires_physical_confirmation: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self):
        return f"<RiskAssessment {self.score}/{self.level} (session:{self.session_id})>"