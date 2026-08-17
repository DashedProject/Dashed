from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Dashed"
)

app.mount(
    "/",
    StaticFiles(
        directory=".",
        html=True
    ),
)