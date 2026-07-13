from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.logger import logger
from app.websocket.connection_manager import manager
from app.services.event_processor import process_event

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    logger.info("WebSocket client connected")

    try:

        while True:

            data = await websocket.receive_json()

            print(f"\nReceived : {data}")

            await process_event(data)

            await manager.send_personal_message(
                {
                    "status": "received"
                },
                websocket,
            )

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        logger.info("Disconnected")