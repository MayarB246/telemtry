# parser.py
from models import Telemetry
from datetime import datetime, timezone

def parse_simulated_packet(raw: dict) -> Telemetry:
    """
    Recebe um dicionário bruto e converte para Telemetry
    """
    return Telemetry(
        timestamp=datetime.now(timezone.utc),

        apps1=raw["apps1"],
        apps2=raw["apps2"],

        bpps1=raw["bpps1"],
        bpps2=raw["bpps2"],

        steering_angle=raw["steering_angle"],

        susp_fl=raw["susp_fl"],
        susp_fr=raw["susp_fr"],
        susp_rl=raw["susp_rl"],
        susp_rr=raw["susp_rr"],

        accel_x=raw["accel_x"],
        accel_y=raw["accel_y"],
        gyro_z=raw["gyro_z"],

        speed=raw["speed"],
        battery_temp=raw["battery_temp"],
    )
