from datetime import datetime
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field, field_validator

class EventRequest(BaseModel):
    """Schema for incoming event data (API request)."""
    
    event_id: str = Field(..., description="Unique event identifier")
    session_id: str = Field(..., description="Associated session ID")
    event_type: str = Field(..., description="Type/category of event")
    timestamp: datetime = Field(..., description="When event occurred")
    source_app: str = Field(..., description="Originating application")
    payload: dict[str, Any] = Field(default_factory=dict, description="Event-specific data")

    @field_validator('timestamp')
    def validate_timestamp(cls, v: datetime) -> datetime:
        if v > datetime.now():
            raise ValueError("Event timestamp cannot be in the future")
        return v

class EventResponse(BaseModel):
    """Schema for API responses after event processing."""
    
    status: Literal["success", "error"] = Field(..., description="Processing outcome")
    message: Optional[str] = Field(None, description="Additional context about the result")