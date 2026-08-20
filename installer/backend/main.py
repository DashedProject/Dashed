from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess

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
    return installer.get_disks()


@app.get("/disks/{device_name}")
def disk(device_name: str):
    device = f"/dev/{device_name}"

    try:
        return installer.get_disk(device)

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Disk not found"
        )


@app.post("/install")
def install(config: dict):
    try:
        return installer.install(config)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except subprocess.CalledProcessError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Partitioning failed: {error}"
        )