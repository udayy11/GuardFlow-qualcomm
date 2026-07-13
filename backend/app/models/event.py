from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class Event(Base):
    """Event model representing system events.

    Attributes:
        id: Primary key UUID
        session_id: Tracking identifier for event sessions
        event_type: Category of event (e.g., 'user_action', 'system_alert')
        source_app: Originating application name
        timestamp: When the event occurred in the source system
        payload: Flexible event data storage
        created_at: When the record was created in database
    """

    __tablename__ = "events"
    __table_args__ = (
        Index("ix_events_session_id", "session_id"),
        Index("ix_events_event_type", "event_type"),
    )

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
        server_default=text("gen_random_uuid()"),
    )
    session_id: Mapped[str] = mapped_column(index=True)
    event_type: Mapped[str] = mapped_column(index=True)
    source_app: Mapped[str]
    timestamp: Mapped[datetime]
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self):
        return f"<Event {self.event_type}@{self.timestamp}>"