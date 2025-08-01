from fastapi import FastAPI
from app.routers import predict # Import your router

app = FastAPI(
    title="Simple ML API",
    description="A basic example of a modular FastAPI application for ML predictions.",
    version="0.1.0"
)

# Include the router for predictions. All routes in predict.py will be under /api/v1
app.include_router(predict.router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Root endpoint to welcome users.
    """
    return {"message": "Welcome to the Simple ML API! Visit /docs for interactive documentation."}