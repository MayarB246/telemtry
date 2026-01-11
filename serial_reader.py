# serial_reader.py
import time
import random
from parser import parse_simulated_packet
from storage import add_telemetry
from db_writer import save_telemetry

# --- Variáveis de Memória (Globais para a sessão) ---
packet_counter = 0
start_time = time.time()
last_loop_time = time.time()

# Acumuladores
total_distance_km = 0.0
total_energy_kWh = 0.0
acc_speed = 0.0
acc_power = 0.0
samples_count = 0

def start():
    global packet_counter, last_loop_time, samples_count
    global total_distance_km, total_energy_kWh, acc_speed, acc_power

    print("Serial reader iniciado (SIMULAÇÃO COM ESTATÍSTICAS)")

    while True:
        # 1. Controle de Tempo (Delta T)
        current_time = time.time()
        dt_seconds = current_time - last_loop_time
        dt_hours = dt_seconds / 3600.0  # Para converter em km/h e kWh
        last_loop_time = current_time

        packet_counter += 1
        samples_count += 1

        # 2. Gerar valores instantâneos (Extraídos para variaveis para podermos calcular)
        inst_speed = random.uniform(0.0, 90.0)
        inst_voltage = random.uniform(250.0, 400.0)
        inst_current = random.uniform(-50.0, 200.0)
        inst_temp = random.uniform(25.0, 60.0)
        
        # Potência (kW) = (V * A) / 1000
        inst_power_kw = (inst_voltage * inst_current) / 1000.0

        # 3. Cálculos de Acumulados (Integrais e Médias)
        # Distância = Velocidade * Tempo
        total_distance_km += inst_speed * dt_hours
        
        # Energia = Potência * Tempo
        # (Se a corrente for negativa/regenerativa, a energia diminui ou mantém, depende da lógica. Aqui soma tudo)
        total_energy_kWh += abs(inst_power_kw) * dt_hours 

        acc_speed += inst_speed
        acc_power += inst_power_kw

        # Médias
        avg_speed = acc_speed / samples_count
        avg_power = acc_power / samples_count

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
            "steering_angle": random.uniform(-450.0, 450.0),  
            "speed": inst_speed,  # <--- Usando a variável gerada acima

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
            "accel_x": random.uniform(-3.0, 3.0),   
            "accel_y": random.uniform(-3.0, 3.0),   
            "gyro_z": random.uniform(-250.0, 250.0),

            # ======================
            # Bateria / BMS
            # ======================
            "battery_temp": inst_temp,       # <--- Variável
            "battery_voltage": inst_voltage, # <--- Variável
            "battery_current": inst_current, # <--- Variável
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
            # Sistema & NOVOS DADOS
            # ======================
            "packet_counter": packet_counter,
            "lora_rssi": random.randint(-120, -40),
            "source": "sim",

            # --- DADOS ADICIONADOS (ESTRUTURA PLANA) ---
            "total_distance": total_distance_km,
            "total_energy": total_energy_kWh,
            "avg_speed": avg_speed,
            "avg_power": avg_power,
            "session_time": current_time - start_time
        }

        # Parser padroniza o pacote
        telemetry = parse_simulated_packet(raw_packet)

        # Armazena no buffer (futuro backend/web)
        add_telemetry(telemetry)
        ## save_telemetry(telemetry)

        # Pequeno print para você conferir se está calculando
        print(f"Distância: {total_distance_km:.3f} km | Energia: {total_energy_kWh:.4f} kWh")

        time.sleep(2.0)  # Aumentei a velocidade para 10Hz (0.1s) para a simulação ficar mais fluida

if __name__ == "__main__":
    start()