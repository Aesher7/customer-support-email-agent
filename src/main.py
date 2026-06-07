"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from src.api.routes import router
from src.core.config import get_settings
from src.core.logger import setup_logger
from src.db.database import init_db

logger = setup_logger(__name__)

settings = get_settings()

app = FastAPI(
    title="Customer Support Email Agent",
    description="AI-powered customer support email processing system",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Include admin routes
from src.api.admin import router as admin_router
app.include_router(admin_router)

# Mount static files
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.get("/")
async def root():
    """Serve the main UI page."""
    return FileResponse(str(Path(__file__).parent.parent / "static" / "index.html"))


@app.on_event("startup")
async def startup():
    """Application startup event."""
    logger.info("Starting Customer Support Email Agent")
    # Initialize database
    init_db()


@app.on_event("shutdown")
async def shutdown():
    """Application shutdown event."""
    logger.info("Shutting down Customer Support Email Agent")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
