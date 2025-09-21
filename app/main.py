import contextlib
import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient # Recommended for async operations
from app.core.config import settings
from app.routers import surgeries

# Use an async context manager for a clean startup/shutdown process
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the application.
    """
    print("Connecting to MongoDB Atlas...")
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    print("Connected to MongoDB Atlas!")
    yield
    print("Closing MongoDB Atlas connection...")
    app.mongodb_client.close()
    print("MongoDB Atlas connection closed!")

# Initialize the FastAPI app with the lifespan context manager
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Include the API router for surgeries
app.include_router(surgeries.router, prefix="/api/v1/surgeries", tags=["surgeries"])

# Define a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Surgery Scheduling API"}

# Entry point for running with Uvicorn, typically used for local development
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
