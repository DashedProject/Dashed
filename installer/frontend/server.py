from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import terminal

app = FastAPI(
    title="Dashed"
)

app.mount(
    "/",
    StaticFiles(
        directory="./static",
        html=True
    ),
)