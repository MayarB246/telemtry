from fastapi import FastAPI
from threading import Thread
from serial_reader import start
from database import init_db, SessionLocal, Telemetry
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    Thread(target=start, daemon=True).start()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/telemetry")
def telemetry(limit: int = 100):
    db = SessionLocal()

    rows = (
        db.query(Telemetry)
        .order_by(Telemetry.id.asc())
        .limit(limit)
        .all()
    )

    db.close()

    return [
        {
            "id": row.id,
            "timestamp": row.timestamp,
            "data": row.data
        }
        for row in rows
    ]
