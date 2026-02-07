from database import SessionLocal, Telemetry

def save_telemetry(telemetry_data: dict):
    db = SessionLocal()
    try:
        row = Telemetry(data=telemetry_data)
        db.add(row)
        db.commit()
    finally:
        db.close()
