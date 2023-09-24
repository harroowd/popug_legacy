from api.v1 import api_router
from config.settings import settings
from fastapi import FastAPI

from popug_legacy_sdk.redis.redis import close_redis, init_redis

app = FastAPI(docs_url="/v1/swagger")


app.include_router(api_router.api_router)


@app.on_event("startup")
async def startup_event():
    await init_redis(
        settings.redis.redis_pool_name, settings.redis.get_redis_url
    )


@app.on_event("shutdown")
async def shutdown_event():
    await close_redis(settings.redis.redis_pool_name)
