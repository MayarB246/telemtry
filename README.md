# Projeto de Telemetria (STM32 + Simulação)

## 🔌 Modo Simulação vs Porta Serial Real (STM32)

Este projeto de telemetria foi desenvolvido para funcionar **mesmo sem o hardware conectado**, utilizando um **modo de simulação**, e permitir a troca fácil para a **porta serial real (COM)** quando o STM32 estiver disponível.

---

## 🧪 Modo Simulação (sem STM32)

O modo simulação permite testar todo o sistema de telemetria:

* Backend (FastAPI)
* Parser de dados
* Armazenamento em memória
* API REST
* Integração web futura

sem a necessidade do microcontrolador conectado.

### ✔ Como funciona

No modo simulação, o sistema **gera pacotes de telemetria automaticamente**, simulando os dados que viriam do STM32 via LoRa/Serial.

Esses dados passam pelo **mesmo parser**, **mesmo armazenamento** e **mesma API**, garantindo que o comportamento seja idêntico ao sistema real.

### ✔ Como ativar a simulação

No arquivo:

```bash
serial_reader.py
```

Certifique-se de que a flag de simulação está ativada:

```python
SIMULATION = True
```

Quando essa opção estiver ativada:

* Nenhuma porta COM será aberta
* Os dados são gerados internamente
* O sistema funciona em qualquer computador

---

## 🔗 Modo Porta Serial Real (STM32 / LoRa)

Quando o STM32 estiver disponível, basta **desativar a simulação** e configurar a porta correta.

### ✔ Como ativar a porta COM real

No mesmo arquivo `serial_reader.py`:

```python
SIMULATION = False
PORT = "COM3"     # Ajustar conforme o sistema
BAUD = 115200     # Deve ser o mesmo do STM32
```

📌 **Importante:**

* A porta COM deve existir no sistema
* Nenhum outro programa pode estar usando a porta
* O baudrate deve ser exatamente igual ao firmware do STM32

Se a porta estiver incorreta ou desconectada, o sistema exibirá um erro ao iniciar.

---

## 🧠 Arquitetura do Código (Dicas Importantes)

### 🔹 Separação de responsabilidades

O projeto foi organizado para facilitar manutenção e evolução:

| Arquivo            | Função                                           |
| ------------------ | ------------------------------------------------ |
| `serial_reader.py` | Leitura serial **ou** simulação de dados         |
| `parser.py`        | Converte strings recebidas em dados estruturados |
| `storage.py`       | Armazena os dados de telemetria em memória       |
| `main.py`          | API FastAPI e inicialização do sistema           |

Essa separação permite:

* trocar LoRa por CAN, Wi-Fi ou Ethernet sem refazer a API
* trocar banco de dados futuramente sem alterar o parser
* testar o sistema sem hardware

---

### 🔹 Armazenamento em memória

Atualmente, os dados são armazenados em um buffer circular:

```python
telemetry_buffer = []
```

* Mantém apenas os últimos **5000 registros**
* Evita consumo excessivo de memória
* Ideal para testes e dashboards em tempo real

📌 Em versões futuras, este módulo pode ser substituído por:

* SQLite
* PostgreSQL
* InfluxDB
* API externa

sem alterar o restante do sistema.