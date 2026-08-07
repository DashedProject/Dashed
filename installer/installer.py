import subprocess
import signal
import sys

processes = []

try:
    processes.append(
        subprocess.Popen([
            "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "7001"
        ], cwd="backend",
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        )
    )
    

    processes.append(
        subprocess.Popen([
            "uvicorn",
            "server:app",
            "--host", "0.0.0.0",
            "--port", "8001"
        ], cwd="frontend",
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        )
    )

    for process in processes:
        process.wait()

finally:
    for process in processes:
        process.terminate()

    sys.exit(0)