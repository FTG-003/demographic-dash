/**
 * js/charts.js — Configurazioni e creazione di tutti i grafici Chart.js
 * (mainChart, europeChart, regionsChart, ageChart, projectionChart, causesChart)
 * Italian Demographic Observatory v1.4+
 */

/* ── Init Chart.js global theme ── */

function initChartDefaults() {
  Chart.defaults.color = 'rgba(240, 230, 216, 0.55)';
  Chart.defaults.borderColor = 'rgba(42, 58, 92, 0.25)';
  Chart.defaults.font.family = "'Outfit', 'Inter', -apple-system, sans-serif";
  Chart.register(ChartDataLabels);
  if (typeof ChartAnnotation !== 'undefined') {
    Chart.register(ChartAnnotation);
  }
}

/* ── Init all 6 charts ── */

function initCharts() {
  // Prevent double init
  if (window.__chartsInitialized) return;
  window.__chartsInitialized = true;

  initChartDefaults();

  var obs = DATA.observations;

  /* ─── 1. Main Chart: nascite (smeraldo) + decessi (rosso) + TFR (blu) ─── */
  var mainCtx = getEl('mainChart').getContext('2d');
  var mH = mainCtx.canvas.parentElement.clientHeight || 440;
  var gradB = mainCtx.createLinearGradient(0, 0, 0, mH);
  gradB.addColorStop(0, 'rgba(16,185,129,0.25)');
  gradB.addColorStop(1, 'rgba(16,185,129,0.0)');
  var gradT = mainCtx.createLinearGradient(0, 0, 0, mH);
  gradT.addColorStop(0, 'rgba(59,130,246,0.25)');
  gradT.addColorStop(1, 'rgba(59,130,246,0.0)');

  var mainChart = new Chart(mainCtx, {
    type: 'line',
    data: {
      labels: obs.births.years,
      datasets: [
        {
          label: 'Nati vivi (migliaia)',
          data: obs.births.values,
          borderColor: '#10B981',
          backgroundColor: gradB,
          borderWidth: 2.5,
          tension: 0.3,
          fill: true,
          yAxisID: 'y',
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBackgroundColor: '#10B981',
          pointBorderColor: 'rgba(240,230,216,0.2)',
          pointBorderWidth: 1,
        },
        {
          label: 'Decessi annuali (migliaia)',
          data: obs.deaths.values,
          borderColor: '#DC2626',
          backgroundColor: 'rgba(220,38,38,0.08)',
          borderWidth: 2.5,
          borderDash: [8, 4],
          tension: 0.3,
          fill: true,
          yAxisID: 'y',
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBackgroundColor: '#DC2626',
          pointBorderColor: 'rgba(240,230,216,0.2)',
          pointBorderWidth: 1,
        },
        {
          label: 'TFR (figli per donna)',
          data: obs.fertility.values,
          borderColor: '#3B82F6',
          backgroundColor: gradT,
          borderWidth: 2.5,
          tension: 0.3,
          fill: true,
          yAxisID: 'y1',
          pointRadius: 3.5,
          pointHoverRadius: 7,
          pointBackgroundColor: '#3B82F6',
          pointBorderColor: 'rgba(240,230,216,0.2)',
          pointBorderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          labels: { usePointStyle: true, padding: 16, font: { size: 12 } },
        },
        tooltip: {
          backgroundColor: 'rgba(14,19,41,0.95)',
          titleColor: 'rgba(240,230,216,0.55)',
          bodyColor: '#F0E6D8',
          borderColor: 'rgba(42,58,92,0.5)',
          borderWidth: 1,
          cornerRadius: 8,
          padding: 12,
          caretPadding: 6,
          callbacks: {
            title: function (ctx) {
              return 'Anno ' + ctx[0].label;
            },
            label: function (ctx) {
              if (ctx.datasetIndex === 0)
                return 'Nascite: ' + ctx.parsed.y.toLocaleString('it-IT') + 'K';
              if (ctx.datasetIndex === 1)
                return (
                  'Decessi: ' +
                  ctx.parsed.y
                    .toLocaleString('it-IT')
                    .replace('.', ',') +
                  'K'
                );
              return 'TFR: ' + ctx.parsed.y.toFixed(2);
            },
            afterBody: function (ctx) {
              var bIdx = -1,
                dIdx = -1;
              ctx.forEach(function (c, i) {
                if (c.datasetIndex === 0) bIdx = c.dataIndex;
                if (c.datasetIndex === 1) dIdx = c.dataIndex;
              });
              if (bIdx >= 0 && dIdx >= 0) {
                var births = obs.births.values[bIdx];
                var deaths = obs.deaths.values[dIdx];
                var saldo = births - deaths;
                var segno = saldo >= 0 ? '+' : '';
                return (
                  'Saldo naturale: ' +
                  segno +
                  saldo.toLocaleString('it-IT', {
                    minimumFractionDigits: 1,
                    maximumFractionDigits: 1,
                  }) +
                  'K'
                );
              }
              return [];
            },
          },
        },
        datalabels: { display: false },
        annotation: {
          annotations: {
            replacementLine: {
              type: 'line',
              yMin: obs.fertility_threshold.value,
              yMax: obs.fertility_threshold.value,
              yScaleID: 'y1',
              borderColor: 'rgba(245,158,11,0.5)',
              borderWidth: 2,
              borderDash: [6, 4],
              label: {
                display: true,
                content:
                  'Soglia sostituzione: ' +
                  obs.fertility_threshold.value.toFixed(1).replace('.', ','),
                position: 'end',
                backgroundColor: 'rgba(245,158,11,0.15)',
                color: '#F59E0B',
                font: { size: 11 },
              },
            },
          },
        },
      },
      scales: {
        x: {
          grid: { color: 'rgba(42,58,92,0.2)' },
          ticks: {
            color: 'rgba(240,230,216,0.4)',
            font: { size: 11, family: "'Outfit', 'Inter', sans-serif" },
            maxTicksLimit: 15,
          },
        },
        y: {
          type: 'linear',
          position: 'left',
          title: {
            display: true,
            text: 'Nascite / Decessi (migliaia)',
            color: '#10B981',
            font: {
              size: 12,
              family: "'Outfit', 'Inter', sans-serif",
            },
          },
          ticks: {
            color: '#10B981',
            callback: function (v) {
              return v + 'K';
            },
          },
          grid: { color: 'rgba(16,185,129,0.08)' },
        },
        y1: {
          type: 'linear',
          position: 'right',
          title: {
            display: true,
            text: 'TFR (figli per donna)',
            color: '#3B82F6',
            font: {
              size: 12,
              family: "'Outfit', 'Inter', sans-serif",
            },
          },
          ticks: { color: '#3B82F6' },
          grid: { drawOnChartArea: false },
        },
      },
    },
  });

  getEl('toggleMainChartType').addEventListener('click', function () {
    var isLine = mainChart.config.type === 'line';
    mainChart.config.type = isLine ? 'bar' : 'line';
    mainChart.update();
    var btn = getEl('toggleMainChartType');
    if (btn) btn.textContent = isLine ? '📈' : '📊';
  });

  getEl('downloadMainChart').addEventListener('click', function () {
    downloadChart('mainChart', 'evoluzione_demografica');
  });

  /* ─── 2. Europe Chart (Viola/Magenta Elettrico) ─── */
  var euroCtx = getEl('europeChart').getContext('2d');
  var euValNew = obs.fertility_europe.values;
  var euColors = euValNew.map(function (v) {
    if (v >= 1.5) return 'rgba(127,0,255,0.85)';
    if (v >= 1.3) return 'rgba(225,0,255,0.7)';
    return 'rgba(225,0,255,0.45)';
  });
  var euBorders = euValNew.map(function (v) {
    if (v >= 1.5) return '#7F00FF';
    if (v >= 1.3) return '#E100FF';
    return 'rgba(225,0,255,0.6)';
  });

  new Chart(euroCtx, {
    type: 'bar',
    data: {
      labels: obs.fertility_europe.countries,
      datasets: [
        {
          data: euValNew,
          backgroundColor: euColors,
          borderColor: euBorders,
          borderWidth: 2,
          borderRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(14,19,41,0.95)',
          titleColor: 'rgba(240,230,216,0.55)',
          bodyColor: '#F0E6D8',
          borderColor: 'rgba(42,58,92,0.5)',
          borderWidth: 1,
          cornerRadius: 8,
          padding: 10,
          caretPadding: 6,
          callbacks: {
            title: function (ctx) {
              return ctx[0].label;
            },
            label: function (ctx) {
              return 'TFR: ' + ctx.parsed.y.toFixed(2);
            },
          },
        },
        datalabels: {
          anchor: 'end',
          align: 'top',
          color: 'rgba(240,230,216,0.9)',
          font: { weight: 'bold', size: 11, family: "'Inter', sans-serif" },
          formatter: function (v) {
            return v.toFixed(2);
          },
        },
      },
      interaction: { mode: 'index', intersect: true },
      scales: {
        y: {
          beginAtZero: true,
          max: 2,
          ticks: { color: 'rgba(240,230,216,0.4)' },
          grid: { color: 'rgba(42,58,92,0.2)' },
        },
        x: {
          ticks: {
            color: 'rgba(240,230,216,0.4)',
            font: { size: 11 },
          },
          grid: { display: false },
        },
      },
    },
  });

  getEl('downloadEuropeChart').addEventListener('click', function () {
    downloadChart('europeChart', 'confronto_europeo_tfr');
  });

  /* ─── 3. Regions Chart (Viola/Magenta Elettrico) ─── */
  var regCtx = getEl('regionsChart').getContext('2d');
  var regVals = obs.fertility_regions.values;
  var regColors = regVals.map(function (v) {
    if (v >= 1.5) return 'rgba(127,0,255,0.85)';
    if (v >= 1.3) return 'rgba(225,0,255,0.7)';
    return 'rgba(225,0,255,0.45)';
  });
  var regBorders = regVals.map(function (v) {
    if (v >= 1.5) return '#7F00FF';
    if (v >= 1.3) return '#E100FF';
    return 'rgba(225,0,255,0.6)';
  });

  new Chart(regCtx, {
    type: 'bar',
    data: {
      labels: obs.fertility_regions.regions,
      datasets: [
        {
          data: regVals,
          backgroundColor: regColors,
          borderColor: regBorders,
          borderRadius: 8,
          borderWidth: 2,
        },
      ],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(14,19,41,0.95)',
          titleColor: 'rgba(240,230,216,0.55)',
          bodyColor: '#F0E6D8',
          borderColor: 'rgba(42,58,92,0.5)',
          borderWidth: 1,
          cornerRadius: 8,
          padding: 10,
          caretPadding: 6,
          callbacks: {
            title: function (ctx) {
              return ctx[0].label;
            },
            label: function (ctx) {
              return 'TFR: ' + ctx.parsed.x.toFixed(2);
            },
          },
        },
        datalabels: {
          anchor: 'end',
          align: 'right',
          color: 'rgba(240,230,216,0.9)',
          font: { weight: 'bold', size: 11, family: "'Inter', sans-serif" },
          formatter: function (v) {
            return v.toFixed(2);
          },
        },
      },
      interaction: { mode: 'index', intersect: true },
      scales: {
        x: {
          beginAtZero: true,
          max: 1.5,
          ticks: { color: 'rgba(240,230,216,0.4)' },
          grid: { color: 'rgba(42,58,92,0.2)' },
        },
        y: {
          ticks: {
            color: 'rgba(240,230,216,0.4)',
            font: { size: 11 },
          },
          grid: { display: false },
        },
      },
    },
  });

  getEl('downloadRegionsChart').addEventListener('click', function () {
    downloadChart('regionsChart', 'tfr_regionale');
  });

  /* ─── 4. Age Structure Chart (Ciano/Smeraldo Invecchiamento) ─── */
  var ageCtx = getEl('ageChart').getContext('2d');
  new Chart(ageCtx, {
    type: 'polarArea',
    data: {
      labels: obs.age_structure.categories,
      datasets: [
        {
          data: obs.age_structure.values,
          backgroundColor: [
            'rgba(0,242,254,0.7)',
            'rgba(79,172,254,0.7)',
            'rgba(37,117,252,0.7)',
            'rgba(107,72,255,0.7)',
            'rgba(127,0,255,0.7)',
          ],
          borderColor: 'rgba(255,255,255,0.3)',
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: 'rgba(240,230,216,0.55)',
            font: { size: 11, family: "'Inter', sans-serif" },
          },
        },
        datalabels: {
          color: 'rgba(240,230,216,0.9)',
          font: {
            weight: 'bold',
            size: 12,
            family: "'Inter', sans-serif",
          },
          formatter: function (v) {
            return v + '%';
          },
        },
      },
      scales: {
        r: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { display: false },
        },
      },
    },
  });

  /* ─── 5. Projections Chart (Ciano/Smeraldo) ─── */
  var projCtx = getEl('projectionChart').getContext('2d');
  var proj = obs.projections;

  new Chart(projCtx, {
    type: 'line',
    data: {
      labels: proj.years,
      datasets: [
        {
          label: 'Scenario ottimista',
          data: proj.scenarios.ottimista,
          borderColor: 'rgba(0,242,254,0.6)',
          borderDash: [5, 5],
          borderWidth: 2,
          fill: false,
          tension: 0.3,
          pointRadius: 4,
          pointBackgroundColor: 'rgba(0,242,254,0.6)',
        },
        {
          label: 'Scenario mediano (ISTAT)',
          data: proj.scenarios.base,
          borderColor: '#00F2FE',
          borderWidth: 3,
          fill: false,
          tension: 0.3,
          pointRadius: 5,
          pointBackgroundColor: '#00F2FE',
        },
        {
          label: 'Scenario pessimista',
          data: proj.scenarios.pessimista,
          borderColor: 'rgba(79,172,254,0.6)',
          borderDash: [5, 5],
          borderWidth: 2,
          fill: false,
          tension: 0.3,
          pointRadius: 4,
          pointBackgroundColor: 'rgba(79,172,254,0.6)',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: 'rgba(240,230,216,0.55)',
            font: { size: 11, family: "'Inter', sans-serif" },
          },
        },
        datalabels: { display: false },
      },
      scales: {
        y: {
          min: 45,
          max: 60,
          ticks: {
            color: 'rgba(240,230,216,0.4)',
            callback: function (v) {
              return v + 'M';
            },
          },
          grid: { color: 'rgba(42,58,92,0.2)' },
        },
        x: {
          ticks: { color: 'rgba(240,230,216,0.4)' },
          grid: { color: 'rgba(42,58,92,0.2)' },
        },
      },
    },
  });

  /* ─── 6. Causes Chart (Ambra/Oro Fattori) ─── */
  var causesCtx = getEl('causesChart').getContext('2d');
  var causesData = obs.causes;

  new Chart(causesCtx, {
    type: 'radar',
    data: {
      labels: causesData.categories,
      datasets: [
        {
          label: 'Impatto relativo (stima qualitativa)',
          data: causesData.values,
          borderColor: '#FFB75E',
          backgroundColor: 'rgba(255,183,94,0.15)',
          pointBackgroundColor: '#FFB75E',
          pointBorderColor: 'rgba(240,230,216,0.3)',
          borderWidth: 2.5,
          pointRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: 'rgba(240,230,216,0.55)',
            font: { size: 10, family: "'Inter', sans-serif" },
          },
        },
        datalabels: { display: false },
      },
      scales: {
        r: {
          angleLines: { color: 'rgba(42,58,92,0.25)' },
          grid: { color: 'rgba(42,58,92,0.2)' },
          pointLabels: {
            color: 'rgba(240,230,216,0.55)',
            font: { size: 10, family: "'Inter', sans-serif" },
          },
          ticks: { display: false, stepSize: 20 },
          suggestedMin: 0,
          suggestedMax: 100,
        },
      },
    },
  });
}
