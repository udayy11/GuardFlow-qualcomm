from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.core.logger import logger, configure_logger
from app.database.database import init_database

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo - tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check router
health_router = APIRouter()
@health_router.get("/health")
async def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

# Startup event
@app.on_event("startup")
async def startup():
    """Application startup lifecycle hook"""
    configure_logger()  # Initialize logger first
    logger.info("Starting application")
    try:
        init_database()  # Initialize database tables
        logger.info("Application startup completed")
    except Exception as e:
        logger.critical(f"Startup failed: {str(e)}")
        raise  # Crash the app if startup fails

# Shutdown event
@app.on_event("shutdown")
async def shutdown():
    """Application shutdown lifecycle hook"""
    logger.info("Shutting down application")

# Register routers
app.include_router(health_router, prefix="/api")