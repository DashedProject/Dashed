from fastapi import FastAPI
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
    return [
        {
            "device": "/dev/nvme0n1",
            "size": "512 GB",
            "model": "Dashed Virtual Disk"
        },
        {
            "device": "/dev/sda",
            "size": "1 TB",
            "model": "Dashed Virtual Disk"
        }
    ]