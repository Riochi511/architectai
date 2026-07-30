from fastapi import FastAPI

from app.config import settings

from app.api.users import router as users_router
from app.api.projects import router as projects_router
from app.api.requirements import router as requirements_router
from app.api.architectures import router as architectures_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.get("/")
def root():
    return {
        "message": "Welcome to ArchitectAI",
        "version": settings.APP_VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
    }


app.include_router(users_router)
app.include_router(projects_router)
app.include_router(requirements_router)
app.include_router(architectures_router)