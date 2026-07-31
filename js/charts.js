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
  gradB.addColorStop(0, COLORS.birthsRgba.replace('1)', '0.25)'));
  gradB.addColorStop(1, COLORS.birthsRgba.replace('1)', '0.0)'));
  var gradT = mainCtx.createLinearGradient(0, 0, 0, mH);
  gradT.addColorStop(0, COLORS.tfrRgba.replace('1)', '0.25)'));
  gradT.addColorStop(1, COLORS.tfrRgba.replace('1)', '0.0)'));

  var mainChart = new Chart(mainCtx, {
    type: 'line',
    data: {
      labels: obs.births.years,
      datasets: [
        {
          label: 'Nascite (migliaia)',
          data: obs.births.values,
          borderColor: COLORS.births,
          backgroundColor: gradB,
          borderWidth: 2.5,
          tension: 0.3,
          fill: true,
          yAxisID: 'y',
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBackgroundColor: COLORS.births,
          pointBorderColor: 'rgba(240,230,216,0.2)',
          pointBorderWidth: 1,
        },
        {
          label: 'Decessi annuali (migliaia)',
          data: obs.deaths.values,
          borderColor: COLORS.deaths,
          backgroundColor: COLORS.deathsFill,
          borderWidth: 2.5,
          borderDash: [8, 4],
          tension: 0.3,
          fill: true,
          yAxisID: 'y',
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBackgroundColor: COLORS.deaths,
          pointBorderColor: 'rgba(240,230,216,0.2)',
          pointBorderWidth: 1,
        },
        {
          label: 'TFR (figli per donna)',
          data: obs.fertility.values,
          borderColor: COLORS.tfr,
          backgroundColor: gradT,
          borderWidth: 2.5,
          tension: 0.3,
          fill: true,
          yAxisID: 'y1',
          pointRadius: 3.5,
          pointHoverRadius: 7,
          pointBackgroundColor: COLORS.tfr,
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
                content: [
                  'Soglia di sostituzione',
                  obs.fertility_threshold.value.toFixed(1).replace('.', ',') +
                    ' figli per donna',
                ],
                position: 'end',
                backgroundColor: 'rgba(245,158,11,0.95)',
                color: '#1B2133',
                font: { size: 14, weight: 'bold' },
                padding: { x: 12, y: 8 },
                borderRadius: 8,
                yAdjust: -14,
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
            color: COLORS.births,
            font: {
              size: 12,
              family: "'Outfit', 'Inter', sans-serif",
            },
          },
          ticks: {
            color: COLORS.births,
            callback: function (v) {
              return v + 'K';
            },
          },
          grid: { color: COLORS.birthsRgba.replace('1)', '0.08)') },
        },
        y1: {
          type: 'linear',
          position: 'right',
          title: {
            display: true,
            text: 'TFR (figli per donna)',
            color: COLORS.tfr,
            font: {
              size: 12,
              family: "'Outfit', 'Inter', sans-serif",
            },
          },
          ticks: { color: COLORS.tfr },
          grid: { drawOnChartArea: false },
        },
      },
    },
  });

  var toggleBtn = getEl('toggleMainChartType');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      var isLine = mainChart.config.type === 'line';
      mainChart.config.type = isLine ? 'bar' : 'line';
      mainChart.update();
      toggleBtn.textContent = isLine ? '📈' : '📊';
    });
  }

  var dlMainBtn = getEl('downloadMainChart');
  if (dlMainBtn) {
    dlMainBtn.addEventListener('click', function () {
      downloadChart('mainChart', 'evoluzione_demografica');
    });
  }

  /* ─── 2. Europe Chart (Viola/Magenta Elettrico) ─── */
  var euroCtx = getEl('europeChart').getContext('2d');
  var euValNew = obs.fertility_europe.values;
  var euColors = euValNew.map(function (v) {
    return barColor(v, 1.5, 1.3);
  });
  var euBorders = euValNew.map(function (v) {
    return barBorder(v, 1.5, 1.3);
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

  var dlEuBtn = getEl('downloadEuropeChart');
  if (dlEuBtn) {
    dlEuBtn.addEventListener('click', function () {
      downloadChart('europeChart', 'confronto_europeo_tfr');
    });
  }

  /* ─── 3. Regions Chart (Viola/Magenta Elettrico) ─── */
  var regCtx = getEl('regionsChart').getContext('2d');
  var regVals = obs.fertility_regions.values;
  var regColors = regVals.map(function (v) {
    return barColor(v, 1.5, 1.3);
  });
  var regBorders = regVals.map(function (v) {
    return barBorder(v, 1.5, 1.3);
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

  var dlRegBtn = getEl('downloadRegionsChart');
  if (dlRegBtn) {
    dlRegBtn.addEventListener('click', function () {
      downloadChart('regionsChart', 'tfr_regionale');
    });
  }

  /* ─── 4. Age Structure Chart (5 classi ISTAT 2025 — Ciano/Smeraldo/Viola) ─── */
  var ageCtx = getEl('ageChart').getContext('2d');
  var ageData = obs.age_structure_2025 || obs.age_structure;
  var ageLabels = ageData.labels || ageData.categories;
  var ageValues = ageData.values;
  var agePopolazione = 58.94; // milioni 2025
  var popEstimates = ageValues.map(function (v) { return (v / 100 * agePopolazione).toFixed(2); });

  new Chart(ageCtx, {
    type: 'bar',
    data: {
      labels: ageLabels,
      datasets: [
        {
          data: ageValues,
          backgroundColor: [
            'rgba(0, 242, 254, 0.75)',   // 0-14: ciano brillante
            'rgba(0, 188, 212, 0.75)',   // 15-39: ciano medio
            'rgba(16, 185, 129, 0.70)',  // 40-64: smeraldo
            'rgba(127, 0, 255, 0.70)',   // 65-79: viola
            'rgba(80, 0, 160, 0.80)',    // 80+: viola profondo
          ],
          borderColor: [
            'rgba(0, 242, 254, 0.9)',
            'rgba(0, 188, 212, 0.9)',
            'rgba(16, 185, 129, 0.9)',
            'rgba(127, 0, 255, 0.9)',
            'rgba(80, 0, 160, 0.9)',
          ],
          borderWidth: 2,
          borderRadius: 4,
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
          padding: 12,
          caretPadding: 6,
          callbacks: {
            title: function (ctx) {
              return ctx[0].label;
            },
            label: function (ctx) {
              var idx = ctx.dataIndex;
              return ctx.parsed.y.toFixed(1) + '%  (~' + popEstimates[idx] + 'M)';            },
          },
        },
        datalabels: {
          anchor: 'end',
          align: 'top',
          color: 'rgba(240,230,216,0.9)',
          font: {
            weight: 'bold',
            size: 12,
            family: "'Inter', sans-serif",
          },
          formatter: function (v) {
            return v.toFixed(1) + '%';
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 45,
          ticks: {
            color: 'rgba(240,230,216,0.4)',
            callback: function (v) { return v + '%'; },
          },
          grid: { color: 'rgba(42,58,92,0.2)' },
        },
        x: {
          ticks: {
            color: 'rgba(240,230,216,0.55)',
            font: { size: 10, family: "'Inter', sans-serif" },
          },
          grid: { display: false },
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
          borderColor: COLORS.projOptimistic,
          borderDash: [5, 5],
          borderWidth: 2,
          fill: false,
          tension: 0.3,
          pointRadius: 4,
          pointBackgroundColor: COLORS.projOptimistic,
        },
        {
          label: 'Scenario mediano (ISTAT)',
          data: proj.scenarios.base,
          borderColor: COLORS.projBase,
          borderWidth: 3,
          fill: false,
          tension: 0.3,
          pointRadius: 5,
          pointBackgroundColor: COLORS.projBase,
        },
        {
          label: 'Scenario pessimista',
          data: proj.scenarios.pessimista,
          borderColor: COLORS.projPessimistic,
          borderDash: [5, 5],
          borderWidth: 2,
          fill: false,
          tension: 0.3,
          pointRadius: 4,
          pointBackgroundColor: COLORS.projPessimistic,
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
          borderColor: COLORS.radarBorder,
          backgroundColor: COLORS.radarFill,
          pointBackgroundColor: COLORS.radarPoint,
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
