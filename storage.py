# storage.py
from datetime import datetime
from database import SessionLocal, Telemetry


def add_telemetry(data: dict):
    """
    Salva um pacote de telemetria no banco de dados
    """

    db = SessionLocal()

    try:
        row = Telemetry(
            timestamp=datetime.utcnow(),
            data=data
        )

        db.add(row)
        db.commit()

    except Exception as e:
        print("Erro ao salvar telemetria:", e)
        db.rollback()

    finally:
        db.close()
