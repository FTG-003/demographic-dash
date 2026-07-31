/**
 * js/kpi.js — Inizializzazione KPI e contatori animati CountUp.js
 * Italian Demographic Observatory v1.4+
 */

/**
 * Riduce la dimensione del valore KPI solo se non ci sta nella card
 * (i numeri in mono non possono andare a capo). Risolve il caso es. "355.000"
 * nelle card compatte: si scala solo il numero, mai il layout circostante.
 * @param {HTMLElement} el - elemento .kpi-value
 * @param {HTMLElement} card - elemento .kpi-card contenitore
 */
function fitKpiValue(el, card) {
  if (!el || !card) return;
  var style = el.style;
  var avail =
    card.clientWidth -
    parseFloat(getComputedStyle(card).paddingLeft || 0) -
    parseFloat(getComputedStyle(card).paddingRight || 0);
  // Targget: il testo occupa al massimo il 90% della larghezza disponibile
  var target = avail * 0.9;
  var fontSize = 360; // 3.6rem
  // Diminuisci finché il testo entra (min 0.5rem = 8px)
  while (fontSize > 8) {
    el.style.fontSize = fontSize / 10 + 'rem';
    if (el.scrollWidth <= target) break;
    fontSize -= 4;
  }
  if (fontSize <= 8) {
    // Fallback: ripristina la dimensione fluida del CSS
    style.fontSize = '';
    style.removeProperty('font-size');
  }
}

/**
 * Applica fitKpiValue a tutte le card KPI.
 * @param {boolean} [onlyAnimated] - se true, riallinea solo le card animate da CountUp
 */
function fitAllKpiValues(onlyAnimated) {
  document.querySelectorAll('.kpi-card').forEach(function (card) {
    if (onlyAnimated && card.getAttribute('data-countup') !== 'running') return;
    var el = card.querySelector('.kpi-value');
    if (el) fitKpiValue(el, card);
  });
}

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
  // CountUp 2.8 espone la classe in due modi a seconda del build servito dal CDN:
  //  - ESM/UMS via jsdelivr "countUp.min.js": window.CountUp (o window.countUp.CountUp)
  //  - UMD "countUp.umd.js": window.countUp.CountUp
  var CountUpClass = window.CountUp || (window.countUp && window.countUp.CountUp);
  if (typeof CountUpClass !== 'function') {
    // CountUp non disponibile: il valore è già quello finale (impostato da initKPIs),
    // quindi basta un fit.
    fitAllKpiValues();
    return;
  }
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
      var el = getEl(c.id);
      var card = el.closest('.kpi-card');
      if (card) card.setAttribute('data-countup', 'running');
      var cu = new CountUpClass(c.id, c.end, {
        decimals: c.decimals,
        suffix: c.suffix || '',
        duration: prefersReduced ? 0 : 2,
        useEasing: !prefersReduced,
        useGrouping: c.id === 'kpiBirths',
        onCompleteCallback: function () {
          if (card) card.removeAttribute('data-countup');
          // Alla fine dell'animazione il numero è stabile: ridimensiona se serve
          fitAllKpiValues();
        },
      });
      cu.start();
    } catch (e) {
      // silently ignore CountUp errors for missing elements
    }
  });
}
