# serial_reader.py
import time
import random
from parser import parse_simulated_packet
from storage import add_telemetry
from db_writer import save_telemetry

packet_counter = 0

def start():
    global packet_counter
    print("Serial reader iniciado (SIMULAÇÃO)")

    while True:
        packet_counter += 1

        raw_packet = {
            # ======================
            # Pedais (0.0 – 1.0)
            # ======================
            "apps1": random.uniform(0.0, 1.0),
            "apps2": random.uniform(0.0, 1.0),
            "bpps1": random.uniform(0.0, 1.0),
            "bpps2": random.uniform(0.0, 1.0),

            # ======================
            # Direção e dinâmica
            # ======================
            "steering_angle": random.uniform(-450.0, 450.0),  # graus
            "speed": random.uniform(0.0, 90.0),               # km/h

            # ======================
            # Suspensão (mm)
            # ======================
            "susp_fl": random.uniform(0.0, 50.0),
            "susp_fr": random.uniform(0.0, 50.0),
            "susp_rl": random.uniform(0.0, 50.0),
            "susp_rr": random.uniform(0.0, 50.0),

            # ======================
            # IMU
            # ======================
            "accel_x": random.uniform(-3.0, 3.0),   # g
            "accel_y": random.uniform(-3.0, 3.0),   # g
            "gyro_z": random.uniform(-250.0, 250.0),# deg/s

            # ======================
            # Bateria / BMS
            # ======================
            "battery_temp": random.uniform(25.0, 60.0),   # °C
            "battery_voltage": random.uniform(250.0, 400.0), # V
            "battery_current": random.uniform(-50.0, 200.0), # A
            "bms_fault": False,

            # ======================
            # Tractive System
            # ======================
            "ts_active": True,
            "ready_to_drive": True,
            "precharge_done": True,
            "tsms": True,
            "msd": True,

            # ======================
            # Freios e segurança
            # ======================
            "brake_pressed": random.choice([True, False]),
            "bspd_active": False,
            "bots": False,
            "shutdown_active": False,
            "imd_fault": False,

            # ======================
            # Sistema
            # ======================
            "packet_counter": packet_counter,
            "lora_rssi": random.randint(-120, -40),
            "source": "sim",
        }

        # Parser padroniza o pacote
        telemetry = parse_simulated_packet(raw_packet)

        # Armazena no buffer (futuro backend/web)
        add_telemetry(telemetry)
        save_telemetry(telemetry)

        time.sleep(2.0)  # 5 Hz
