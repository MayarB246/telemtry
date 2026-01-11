# database.py
from sqlalchemy import create_engine, Column, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Banco local (arquivo)
DATABASE_URL = "sqlite:///telemetry.db"

# Engine com suporte a threads (FastAPI + serial reader)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Guarda TODO o pacote de telemetria (JSON completo)
    data = Column(JSON, nullable=False)


def init_db():
    """Cria as tabelas do banco"""
    Base.metadata.create_all(bind=engine)
