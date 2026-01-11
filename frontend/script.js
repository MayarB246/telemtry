/* ================= CONFIGURAÇÕES ================= */
const CONFIG = {
  apiUrl: "http://127.0.0.1:8000/telemetry",
  interval: 2000,     // 200ms para ficar bem fluido
  maxPoints: 50,     // Quantos pontos manter no histórico do gráfico
  simulation: false  // DESLIGADO: Agora vai ler do seu servidor
};

// Variáveis globais dos gráficos
let charts = {};

/* ================= INICIALIZAÇÃO ================= */
document.addEventListener("DOMContentLoaded", () => {
  initCharts();
  setInterval(updateTelemetry, CONFIG.interval);
});

/* ================= CRIAÇÃO DOS GRÁFICOS ================= */
function initCharts() {
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    interaction: { mode: 'index', intersect: false },
    elements: {
      point: { radius: 0 },
      line: { tension: 0.2, borderWidth: 2 }
    },
    scales: {
      x: { display: false },
      y: {
        grid: { color: '#334155' },
        ticks: { color: '#94a3b8', font: { size: 10 } }
      }
    },
    plugins: { legend: { labels: { color: '#e2e8f0', boxWidth: 10, font: { size: 10 } } } }
  };

  const create = (id, datasets, yMin, yMax) => {
    const ctx = document.getElementById(id).getContext('2d');
    const opts = JSON.parse(JSON.stringify(commonOptions));

    if (yMin !== undefined && yMax !== undefined) {
      opts.scales.y.min = yMin;
      opts.scales.y.max = yMax;
    }

    return new Chart(ctx, {
      type: 'line',
      data: { labels: [], datasets: datasets },
      options: opts
    });
  };

  // Configurando as linhas dos gráficos
  charts.apps = create('appsChart', [
    { label: 'APPS 1 (%)', data: [], borderColor: '#22c55e' },
    { label: 'APPS 2 (%)', data: [], borderColor: '#16a34a' },
    { label: 'BPPS 1 (%)', data: [], borderColor: '#ef4444' }
  ], 0, 100);

  charts.speed = create('speedChart', [
    { label: 'Velocidade (km/h)', data: [], borderColor: '#facc15', backgroundColor: 'rgba(250, 204, 21, 0.1)', fill: true }
  ], 0, 120);

  charts.susp = create('suspChart', [
    { label: 'FL', data: [], borderColor: '#38bdf8' },
    { label: 'FR', data: [], borderColor: '#0ea5e9' },
    { label: 'RL', data: [], borderColor: '#f472b6' },
    { label: 'RR', data: [], borderColor: '#db2777' }
  ]);

  charts.imu = create('imuChart', [
    { label: 'Ax (g)', data: [], borderColor: '#a855f7' },
    { label: 'Ay (g)', data: [], borderColor: '#d946ef' },
    { label: 'Gz', data: [], borderColor: '#cbd5e1', borderDash: [5, 5] } // Adicionei Giroscópio tracejado
  ], -3, 3);

  charts.bat = create('batChart', [
    { label: 'Temp Max (°C)', data: [], borderColor: '#f97316' }
  ], 20, 70);
}

/* ================= LÓGICA DE DADOS ================= */
function pushData(chart, values) {
  const dataArray = Array.isArray(values) ? values : [values];

  chart.data.labels.push('');
  if (chart.data.labels.length > CONFIG.maxPoints) chart.data.labels.shift();

  chart.data.datasets.forEach((dataset, i) => {
    // Se o valor não existir no JSON, usa 0 para não quebrar o gráfico
    const rawVal = dataArray[i];
    const val = typeof rawVal === 'number' ? rawVal : 0;

    dataset.data.push(val);
    if (dataset.data.length > CONFIG.maxPoints) dataset.data.shift();
  });

  chart.update('none');
}

function updateLED(id, isActive) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.remove('active');
  if (isActive) el.classList.add('active');
}

/* ================= FETCH & LOOP (CONEXÃO JSON) ================= */
async function updateTelemetry() {
  console.log("Tentando buscar dados...");
  try {
    const res = await fetch(CONFIG.apiUrl);
    if (!res.ok) throw new Error("Erro HTTP: " + res.status);

    const jsonList = await res.json();

    // SEU JSON É UM ARRAY. Pegamos o índice 0 (o mais recente)
    if (!jsonList || jsonList.length === 0) return;
    const latestPacket = jsonList[0];

    // Atalho para a parte de dados
    const d = latestPacket.data;

    // 1. ATUALIZA TEXTOS (KPIs)
    document.getElementById('kpiSpeed').innerHTML = `${d.speed_kmh.toFixed(1)} <small>km/h</small>`;
    document.getElementById('kpiSteer').innerHTML = `${d.steering_angle_deg.toFixed(1)}<small>°</small>`;
    document.getElementById('kpiVolt').innerHTML = `${d.battery.voltage_v.toFixed(1)} <small>V</small>`;
    document.getElementById('kpiCurr').innerHTML = `${d.battery.current_a.toFixed(1)} <small>A</small>`;
    document.getElementById('kpiBatTemp').innerHTML = `${d.battery.temperature_c.toFixed(1)} <small>°C</small>`;

    // 2. ATUALIZA GRÁFICOS
    // Multiplicamos pedais por 100 pois vem 0.32 (32%)
    pushData(charts.apps, [
      d.apps.apps1 * 100,
      d.apps.apps2 * 100,
      d.bpps.bpps1 * 100
    ]);

    pushData(charts.speed, d.speed_kmh);

    pushData(charts.susp, [
      d.suspension.fl,
      d.suspension.fr,
      d.suspension.rl,
      d.suspension.rr
    ]);

    pushData(charts.imu, [
      d.imu.accel_x,
      d.imu.accel_y,
      d.imu.gyro_z / 100 // Dividi por 100 só para caber na escala visual, ajuste se necessário
    ]);

    pushData(charts.bat, d.battery.temperature_c);

    // 3. ATUALIZA STATUS (LEDS)
    // Usando os booleanos diretos do seu JSON
    updateLED('ts_active', d.tractive_system.ts_active);
    updateLED('ready_to_drive', d.tractive_system.ready_to_drive);
    updateLED('precharge_done', d.tractive_system.precharge_done);
    updateLED('tsms', d.tractive_system.tsms);
    updateLED('brake_pressed', d.brakes.brake_pressed);
    updateLED('bspd_active', d.brakes.bspd_active);
    updateLED('shutdown_active', d.safety.shutdown_active);
    updateLED('imd_fault', d.safety.imd_fault);

    // Debug simples no console para garantir que chegou
    // console.log("Dados atualizados:", latestPacket.id);

  } catch (error) {
    console.error("Falha ao buscar dados:", error);
    // Opcional: Mostrar aviso na tela se cair a conexão
  }
}