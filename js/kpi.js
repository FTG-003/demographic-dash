/**
 * js/kpi.js — Inizializzazione KPI e contatori animati CountUp.js
 * Italian Demographic Observatory v1.4+
 */

function initKPIs() {
  var obs = DATA.observations;
  // Anno target per i KPI: l'ultimo anno consolidato prima della proiezione.
  // Lo ricaviamo dalla serie nascite (penultimo anno dell'array).
  var targetYear = obs.births.years[obs.births.years.length - 2] || 2025;

  var kpis = [
    {
      id: 'kpiBirths',
      val: (getValueForYear(obs.births, targetYear, 0) * 1000).toLocaleString('it-IT'),
      trendKey: 'births',
    },
    {
      id: 'kpiTfr',
      val: getValueForYear(obs.fertility, targetYear, 0)
        .toFixed(2)
        .replace('.', ','),
      trendKey: 'tfr',
    },
    {
      id: 'kpiElderly',
      val:
        getValueForYear(obs.elderly_ratio, targetYear, obs.elderly_ratio.values[obs.elderly_ratio.values.length - 1])
          .toFixed(1)
          .replace('.', ',') + '%',
      trendKey: 'elderly',
    },
    {
      id: 'kpiPopulation',
      val: getValueForYear(obs.population, targetYear, 0)
        .toFixed(1)
        .replace('.', ','),
      trendKey: 'population',
    },
    {
      id: 'kpiAge',
      val: obs.first_child_age.value.toFixed(1).replace('.', ','),
      trendKey: 'age',
    },
    {
      id: 'kpiDecline',
      val: obs.births_decline.value.toFixed(1).replace('.', ',') + '%',
      trendKey: 'decline',
    },
  ];

  kpis.forEach(function (k) {
    var el = getEl(k.id);
    if (el) el.textContent = k.val;

    var kpiData = obs.kpi && obs.kpi[k.trendKey];
    if (kpiData) {
      var trendEl = getEl(k.id + 'Trend');
      if (trendEl) trendEl.textContent = kpiData.trend;
      var noteEl = getEl(k.id + 'Note');
      if (noteEl) noteEl.textContent = kpiData.note;
    }
  });
}

function initCounters() {
  if (typeof CountUp === 'undefined') return;
  var prefersReduced = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
  ).matches;
  var obs = DATA.observations;

  // Determina l'anno target per i contatori (stessa logica di initKPIs)
  var counterTargetYear = obs.births.years[obs.births.years.length - 2] || 2025;

  var counters = [
    {
      id: 'kpiBirths',
      end: getValueForYear(obs.births, counterTargetYear, 0) * 1000,
      decimals: 0,
      suffix: '',
    },
    {
      id: 'kpiTfr',
      end: getValueForYear(obs.fertility, counterTargetYear, 0),
      decimals: 2,
      suffix: '',
    },
    {
      id: 'kpiElderly',
      end: getValueForYear(obs.elderly_ratio, counterTargetYear, obs.elderly_ratio.values[obs.elderly_ratio.values.length - 1]),
      decimals: 1,
      suffix: '%',
    },
    {
      id: 'kpiPopulation',
      end: getValueForYear(obs.population, counterTargetYear, 0),
      decimals: 1,
      suffix: '',
    },
    {
      id: 'kpiAge',
      end: obs.first_child_age.value,
      decimals: 1,
      suffix: '',
    },
    {
      id: 'kpiDecline',
      end: obs.births_decline.value,
      decimals: 1,
      suffix: '%',
    },
  ];

  counters.forEach(function (c) {
    if (!getEl(c.id)) return;
    try {
      var cu = new CountUp(c.id, c.end, {
        decimals: c.decimals,
        suffix: c.suffix || '',
        duration: prefersReduced ? 0 : 2,
        useEasing: !prefersReduced,
        useGrouping: c.id === 'kpiBirths',
      });
      cu.start();
    } catch (e) {
      // silently ignore CountUp errors for missing elements
    }
  });
}
