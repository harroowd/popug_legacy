from api.v1 import api_router
from fastapi import FastAPI

app = FastAPI(docs_url="/v1/swagger")


app.include_router(api_router.api_router)


def startup() -> FastAPI:
    return app
