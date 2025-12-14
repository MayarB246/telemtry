# models.py
from pydantic import BaseModel
from datetime import datetime, timezone

class Telemetry(BaseModel):
    timestamp: datetime

    apps1: float
    apps2: float

    bpps1: float
    bpps2: float

    steering_angle: float

    susp_fl: float
    susp_fr: float
    susp_rl: float
    susp_rr: float

    accel_x: float
    accel_y: float
    gyro_z: float

    speed: float

    battery_temp: float
