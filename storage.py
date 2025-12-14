# storage.py
MAX_SAMPLES = 5000
telemetry_buffer = []

def add_telemetry(data):
    telemetry_buffer.append(data)
    if len(telemetry_buffer) > MAX_SAMPLES:
        telemetry_buffer.pop(0)

def get_all():
    return telemetry_buffer
