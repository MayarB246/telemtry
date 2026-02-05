const CONFIG = {
    apiUrl: "http://127.0.0.1:8000/telemetry",
    interval: 2000,     
    maxPoints: 50,     // Quantos pontos manter no histórico do gráfico
    simulation: false  // DESLIGADO: Agora vai ler do seu servidor
};

let charts = {};

document.addEventListener("DOMContentLoaded", () => {
    initCharts();
    setInterval(updateTelemetry, CONFIG.interval);
});

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
        { label: 'Gz', data: [], borderColor: '#cbd5e1', borderDash: [5, 5] }
    ], -3, 3);

    charts.bat = create('batChart', [
        { label: 'Temp Max (°C)', data: [], borderColor: '#f97316' }
    ], 20, 70);
}

function pushData(chart, values) {
    const dataArray = Array.isArray(values) ? values : [values];

    chart.data.labels.push('');
    if (chart.data.labels.length > CONFIG.maxPoints) chart.data.labels.shift();

    chart.data.datasets.forEach((dataset, i) => {
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
    
    if (isActive) {
        el.classList.add('active');
    } else {
        el.classList.remove('active');
    }
}

async function updateTelemetry() {
    try {
        const res = await fetch(CONFIG.apiUrl);
        if (!res.ok) throw new Error("Erro HTTP: " + res.status);

        const jsonList = await res.json();
        
        if (!jsonList || jsonList.length === 0) return;

        const latestPacket = jsonList[0];

        let d;
        if (latestPacket.data) {
            d = latestPacket.data;
        } else {
            d = latestPacket;
        }

        
        if (!d.battery || !d.speed_kmh === undefined) {
            console.warn("Estrutura de dados inesperada:", d);
            return;
        }

        if(document.getElementById('kpiSpeed')) document.getElementById('kpiSpeed').innerHTML = `${(d.speed_kmh || 0).toFixed(1)} <small>km/h</small>`;
        if(document.getElementById('kpiSteer')) document.getElementById('kpiSteer').innerHTML = `${(d.steering_angle_deg || 0).toFixed(1)}<small>°</small>`;
        if(document.getElementById('kpiVolt')) document.getElementById('kpiVolt').innerHTML = `${(d.battery?.voltage_v || 0).toFixed(1)} <small>V</small>`;
        if(document.getElementById('kpiCurr')) document.getElementById('kpiCurr').innerHTML = `${(d.battery?.current_a || 0).toFixed(1)} <small>A</small>`;
        if(document.getElementById('kpiBatTemp')) document.getElementById('kpiBatTemp').innerHTML = `${(d.battery?.temperature_c || 0).toFixed(1)} <small>°C</small>`;

        if (d.statistics) {
            const stats = d.statistics;
            const elDist = document.getElementById('statDist');
            if(elDist) elDist.innerText = (stats.total_distance_km || 0).toFixed(3);

            const elEnergy = document.getElementById('statEnergy');
            if(elEnergy) elEnergy.innerText = (stats.total_energy_kwh || 0).toFixed(4);

            const elAvgSpeed = document.getElementById('statAvgSpeed');
            if(elAvgSpeed) elAvgSpeed.innerText = (stats.avg_speed_kmh || 0).toFixed(1);

            const elTime = document.getElementById('statTime');
            if(elTime) elTime.innerText = (stats.session_time_s || 0).toFixed(0);
        }

        if(charts.apps && d.apps && d.bpps) {
            pushData(charts.apps, [
                (d.apps.apps1 || 0) * 100,
                (d.apps.apps2 || 0) * 100,
                (d.bpps.bpps1 || 0) * 100
            ]);
        }

        if(charts.speed) pushData(charts.speed, d.speed_kmh || 0);

        if(charts.susp && d.suspension) {
            pushData(charts.susp, [
                d.suspension.fl || 0,
                d.suspension.fr || 0,
                d.suspension.rl || 0,
                d.suspension.rr || 0
            ]);
        }

        if(charts.imu && d.imu) {
            pushData(charts.imu, [
                d.imu.accel_x || 0,
                d.imu.accel_y || 0,
                (d.imu.gyro_z || 0) / 100 
            ]);
        }

        if(charts.bat && d.battery) pushData(charts.bat, d.battery.temperature_c || 0);

        if(d.tractive_system) {
            updateLED('ts_active', d.tractive_system.ts_active);
            updateLED('ready_to_drive', d.tractive_system.ready_to_drive);
            updateLED('precharge_done', d.tractive_system.precharge_done);
            updateLED('tsms', d.tractive_system.tsms);
        }
        if(d.brakes) {
            updateLED('brake_pressed', d.brakes.brake_pressed);
            updateLED('bspd_active', d.brakes.bspd_active);
        }
        if(d.safety) {
            updateLED('shutdown_active', d.safety.shutdown_active);
            updateLED('imd_fault', d.safety.imd_fault);
        }

    } catch (error) {
        console.error("ERRO NO LOOP DE DADOS:", error);
    }
}