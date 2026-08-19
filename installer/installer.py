import os
import signal
import subprocess
import sys

from frontend.terminal import terminal_ui

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

processes = []

os.system("clear")

def cleanup(signum=None, frame=None):
    for process in processes:
        if process.poll() is None:
            process.terminate()

    for process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

    sys.exit(0)


signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

try:
    processes.append(
        subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "7001",
                "--log-level",
                "critical",
            ],
            cwd=os.path.join(BASE_DIR, "backend"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ))

    processes.append(
        subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "server:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8001",
                "--log-level",
                "critical",
            ],
            cwd=os.path.join(BASE_DIR, "frontend"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            )
        )

    terminal_ui()

    for process in processes:
        process.wait()
    
finally:
    cleanup()