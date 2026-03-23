import logging
from fastapi import FastAPI
from app.routes import router
from app.config import settings

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__) 
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint was called")
    return{"message": "Task API is running"}