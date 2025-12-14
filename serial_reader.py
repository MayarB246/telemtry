# serial_reader.py
import time
import random

from parser import parse_simulated_packet
from storage import add_telemetry

def start():
    print("Serial reader iniciado")

    while True:
        raw = {
            "apps1": random.uniform(0.0, 1.0),
            "apps2": random.uniform(0.0, 1.0),

            "bpps1": random.uniform(0.0, 1.0),
            "bpps2": random.uniform(0.0, 1.0),

            "steering_angle": random.uniform(-450, 450),

            "susp_fl": random.uniform(0, 50),
            "susp_fr": random.uniform(0, 50),
            "susp_rl": random.uniform(0, 50),
            "susp_rr": random.uniform(0, 50),

            "accel_x": random.uniform(-3, 3),
            "accel_y": random.uniform(-3, 3),
            "gyro_z": random.uniform(-250, 250),

            "speed": random.uniform(0, 90),
            "battery_temp": random.uniform(25, 60),
        }

        telemetry = parse_simulated_packet(raw)
        add_telemetry(telemetry)

        time.sleep(0.2)
