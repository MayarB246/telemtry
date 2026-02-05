from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Apps(BaseModel):
    apps1: float
    apps2: float


class Bpps(BaseModel):
    bpps1: float
    bpps2: float


class Suspension(BaseModel):
    fl: float
    fr: float
    rl: float
    rr: float


class IMU(BaseModel):
    accel_x: float
    accel_y: float
    gyro_z: float


class Battery(BaseModel):
    temperature_c: float
    voltage_v: float
    current_a: float
    bms_fault: bool


class TractiveSystem(BaseModel):
    ts_active: bool
    ready_to_drive: bool
    precharge_done: bool
    tsms: bool
    msd: bool


class Brakes(BaseModel):
    brake_pressed: bool
    bspd_active: bool
    bots: bool


class Safety(BaseModel):
    shutdown_active: bool
    imd_fault: bool


class System(BaseModel):
    packet_counter: int
    lora_rssi: Optional[int]
    source: str


class Telemetry(BaseModel):
    timestamp: datetime
    steering_angle_deg: float
    speed_kmh: float

    apps: Apps
    bpps: Bpps
    suspension: Suspension
    imu: IMU
    battery: Battery
    tractive_system: TractiveSystem
    brakes: Brakes
    safety: Safety
    system: System
