from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.tasks import router as tasks_router
from app.exceptions import unexpected_exception_handler


app = FastAPI(
    title="VG Task API",
    description="Task management API",
    version="0.1.0",
)


app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)


@app.get("/")
async def root():
    return {
        "message": "VG Task API"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


app.include_router(auth_router)
app.include_router(tasks_router)