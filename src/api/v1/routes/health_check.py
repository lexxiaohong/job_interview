from fastapi import APIRouter


health_check_router = APIRouter()

@health_check_router.get("/health_check")
async def health_check():
    """
    Health check route for monitoring the app's availability.
    http://127.0.0.1:8000/api/v1/health_check
    """
    print("health check called from health_check.py")
    return {"status": "OK", "message": "Application is running"}