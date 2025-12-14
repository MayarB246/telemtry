# main.py
from fastapi import FastAPI
from threading import Thread
from serial_reader import start
from storage import get_all

app = FastAPI()

@app.on_event("startup")
def startup():
    Thread(target=start, daemon=True).start()

@app.get("/telemetry")
def telemetry():
    return get_all()
