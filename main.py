from fastapi import FastAPI, APIRouter
from src.core.settings import settings

from src.api.v1.resources import users, senders, emails

app = FastAPI(
    title=settings.api.title,
    description=settings.api.description,
    version=settings.api.version,
    docs_url=settings.api.resources.docs.value,
    debug=settings.api.debug
)

router = APIRouter(prefix=settings.api.resources.prefix.value)

router.include_router(router=users.router)
router.include_router(router=senders.router)
router.include_router(router=emails.router)

app.include_router(router=router)


@app.get(settings.api.resources.root.value)
async def root():
    return {
        "service": settings.api.title,
        "version": settings.api.version,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api.host,
        port=settings.api.port
    )
