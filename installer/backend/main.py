from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dashed_install import DashedInstall


app = FastAPI(
    title="Dashed API",
    version="0.0.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


installer = DashedInstall()


@app.get("/status")
def status():
    return installer.get_status()


@app.get("/disks")
def disks():
    try:
        return installer.get_disks()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/install")
def install(config: dict):
    try:
        return installer.install(config)

    except Exception as error:
        installer.status = "failed"

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )