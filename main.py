from fastapi import FastAPI
from threading import Thread
from serial_reader import start
from database import init_db, SessionLocal, Telemetry
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    Thread(target=start, daemon=True).start()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/telemetry")
def telemetry(limit: int = 100):
    db = SessionLocal()

    rows = (
        db.query(Telemetry)
        .order_by(Telemetry.id.desc())
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
