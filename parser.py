# parser.py
from datetime import datetime

def parse_simulated_packet(raw: dict) -> dict:
    """
    Recebe dados crus (simulados ou reais)
    e devolve a telemetria padronizada do sistema
    """

    telemetry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",

        # Pedais
        "apps": {
            "apps1": float(raw.get("apps1", 0.0)),
            "apps2": float(raw.get("apps2", 0.0)),
        },
        "bpps": {
            "bpps1": float(raw.get("bpps1", 0.0)),
            "bpps2": float(raw.get("bpps2", 0.0)),
        },

        # Direção e velocidade
        "steering_angle_deg": float(raw.get("steering_angle", 0.0)),
        "speed_kmh": float(raw.get("speed", 0.0)),

        # Suspensão
        "suspension": {
            "fl": float(raw.get("susp_fl", 0.0)),
            "fr": float(raw.get("susp_fr", 0.0)),
            "rl": float(raw.get("susp_rl", 0.0)),
            "rr": float(raw.get("susp_rr", 0.0)),
        },

        # IMU
        "imu": {
            "accel_x": float(raw.get("accel_x", 0.0)),
            "accel_y": float(raw.get("accel_y", 0.0)),
            "gyro_z": float(raw.get("gyro_z", 0.0)),
        },

        # Bateria / BMS
        "battery": {
            "temperature_c": float(raw.get("battery_temp", 0.0)),
            "voltage_v": float(raw.get("battery_voltage", 0.0)),
            "current_a": float(raw.get("battery_current", 0.0)),
            "bms_fault": bool(raw.get("bms_fault", False)),
        },

        # Tractive System
        "tractive_system": {
            "ts_active": bool(raw.get("ts_active", False)),
            "ready_to_drive": bool(raw.get("ready_to_drive", False)),
            "precharge_done": bool(raw.get("precharge_done", False)),
            "tsms": bool(raw.get("tsms", False)),
            "msd": bool(raw.get("msd", False)),
        },

        # Freios
        "brakes": {
            "brake_pressed": bool(raw.get("brake_pressed", False)),
            "bspd_active": bool(raw.get("bspd_active", False)),
            "bots": bool(raw.get("bots", False)),
        },

        # Segurança
        "safety": {
            "shutdown_active": bool(raw.get("shutdown_active", False)),
            "imd_fault": bool(raw.get("imd_fault", False)),
        },

        # Sistema
        "system": {
            "packet_counter": int(raw.get("packet_counter", 0)),
            "lora_rssi": raw.get("lora_rssi", None),
            "source": raw.get("source", "sim"),
        },
    }

    return telemetry
