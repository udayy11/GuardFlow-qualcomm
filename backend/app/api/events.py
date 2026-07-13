from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.event_schema import EventRequest, EventResponse
from app.services.event_processor import EventProcessor
from app.repositories.event_repository import EventRepository

router = APIRouter(prefix="/events", tags=["events"])

@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Process an event",
    responses={
        201: {"description": "Event processed successfully"},
        400: {"description": "Invalid request data"},
        500: {"description": "Internal processing error"},
    },
)
async def create_event(
    event_data: EventRequest,
    db: Session = Depends(get_db),
) -> EventResponse:
    """Endpoint for submitting system events.
    
    Args:
        event_data: Validated event payload
        db: Database session dependency
        
    Returns:
        Standardized response with processing status
    """
    try:
        processor = EventProcessor(EventRepository(db))
        return processor.process_event(event_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Event processing failed",
        )