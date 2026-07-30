/**
 * js/app.js — Entry-point della dashboard.
 * Ascolta DOMContentLoaded e coordina l'inizializzazione di tutti i moduli
 * nell'ordine corretto.
 * Italian Demographic Observatory v1.4+
 */

/* ── Tabella dati storici ── */

function initTable() {
  var tbody = getEl('dataTableBody');
  if (!tbody) return;
  var html = '';
  var badgeColors = {
    'Picco storico': 'green',
    Ripresa: 'green',
    'Sotto soglia': 'yellow',
    Calo: 'yellow',
    Pandemia: 'yellow',
    Minimo: 'red',
    'Minimo assoluto': 'red',
    'Minimo storico consolidato (355k nati, TFR 1,14)': 'red',
    'Dato parziale / Proiezione ANPR (340k nati)': 'yellow',
  };
  DATA.historicalTable.forEach(function (row) {
    html +=
      '<tr><td>' +
      row.periodo +
      '</td><td>' +
      row.anno +
      '</td><td><strong>' +
      row.nascite.toLocaleString('it-IT') +
      '</strong></td><td>' +
      row.tfr.toFixed(2) +
      '</td><td>' +
      row.natalita.toFixed(1) +
      '‰</td><td><span class="badge ' +
      (badgeColors[row.status] || 'blue') +
      '">' +
      row.status +
      '</span></td></tr>';
  });
  tbody.innerHTML = html;
}

/* ── Changelog ── */

function initChangelog() {
  var container = getEl('changelogContainer');
  if (!container) return;
  var html = '';
  DATA.changelog.forEach(function (entry) {
    html +=
      '<div class="changelog-entry"><span class="changelog-version">v' +
      entry.version +
      '</span><span class="changelog-date">' +
      entry.date +
      '</span><ul class="changelog-changes">';
    entry.changes.forEach(function (c) {
      html += '<li>' + c + '</li>';
    });
    html += '</ul></div>';
  });
  container.innerHTML = html;
}

/* ── Timeline ── */

function initTimeline() {
  var tl = DATA.observations.timeline;
  var descriptions = {};
  Object.keys(tl).forEach(function (k) {
    descriptions[k] = tl[k].description;
  });
  var points = document.querySelectorAll('.timeline-point');
  points.forEach(function (btn) {
    btn.setAttribute(
      'aria-label',
      btn.querySelector('.timeline-event')?.textContent || 'Periodo'
    );
    btn.addEventListener('click', function () {
      var period = btn.getAttribute('data-period');
      var msg =
        descriptions[period] ||
        'Nessuna informazione disponibile per questo periodo.';
      showToast(msg);
      points.forEach(function (p) {
        p.removeAttribute('aria-pressed');
      });
      btn.setAttribute('aria-pressed', 'true');
    });
    btn.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        btn.click();
      }
    });
  });
}

/* ── Metadata — Console stats e versioni ── */

function updateMetadata() {
  var vers = document.querySelectorAll('#dataVersion, #methodologyVersion');
  vers.forEach(function (el) {
    el.textContent = DATA.metadata.dataset_version;
  });

  var updates = document.querySelectorAll(
    '#dataLastUpdate, #methodologyLastUpdate'
  );
  var dateStr = new Date(DATA.metadata.last_update).toLocaleDateString('it-IT', {
    year: 'numeric',
    month: 'long',
  });
  updates.forEach(function (el) {
    el.textContent = dateStr || DATA.metadata.last_update;
  });

  var statusEl = getEl('dataStatus');
  if (statusEl) statusEl.textContent = DATA.metadata.notes;

  // Badge stato condizionale
  var badgeStatus = document.querySelector('.header-badge .dot.yellow');
  if (badgeStatus) {
    var badgeParent = badgeStatus.parentElement;
    if (
      badgeParent &&
      DATA.metadata.notes &&
      DATA.metadata.notes.trim().length > 0
    ) {
      badgeParent.style.display = '';
      if (statusEl) statusEl.textContent = DATA.metadata.notes;
    } else if (badgeParent) {
      badgeParent.style.display = 'none';
    }
  }

  // Titolo dinamico della pagina
  var titleEl = document.querySelector('title');
  if (titleEl) {
    titleEl.textContent =
      'Italian Demographic Observatory v' +
      DATA.metadata.dataset_version +
      ' (' +
      (dateStr || DATA.metadata.last_update) +
      ')';
  }

  var obs = DATA.observations;
  var conBirths = getEl('conBirths');
  if (conBirths)
    conBirths.textContent = formatNum(
      obs.births.values[obs.births.values.length - 1] * 1000,
      0
    ).replace(/,/g, '.');

  var conTfr = getEl('conTfr');
  if (conTfr)
    conTfr.textContent = obs.fertility.values[
      obs.fertility.values.length - 1
    ]
      .toFixed(2)
      .replace('.', ',');

  var conPop = getEl('conPopulation');
  if (conPop)
    conPop.textContent =
      obs.population.values[obs.population.values.length - 1]
        .toFixed(1)
        .replace('.', ',') + ' M';

  var conEld = getEl('conElderly');
  if (conEld)
    conEld.textContent =
      obs.elderly_ratio.values[obs.elderly_ratio.values.length - 1]
        .toFixed(1)
        .replace('.', ',') + '%';

  var kpiAgeVal = getEl('kpiAge');
  var kpiAgeNote = getEl('kpiAgeNote');
  if (kpiAgeVal && obs.first_child_age) {
    var fca = obs.first_child_age;
    kpiAgeVal.textContent = fca.value.toFixed(1).replace('.', ',');
    if (kpiAgeNote)
      kpiAgeNote.textContent = fca.notes || 'Dato ' + fca.year;
  }
}

/* ── Loading Screen ── */

window.addEventListener('load', function () {
  hideLoadingOverlay();
});

// Fallback: se il load event non scatta entro 10 secondi, nascondi comunque
setTimeout(function hideLoadingFallback() {
  hideLoadingOverlay();
}, 10000);

function hideLoadingOverlay() {
  var overlay = getEl('loadingOverlay');
  if (overlay && overlay.classList.contains('open')) {
    var prefersReduced = window.matchMedia(
      '(prefers-reduced-motion: reduce)'
    ).matches;
    var delay = prefersReduced ? 100 : 600;
    setTimeout(function () {
      overlay.classList.remove('open');
    }, delay);
  }
}

/* ── Entry point ── */

document.addEventListener('DOMContentLoaded', function () {
  initKPIs();
  initCounters();
  initCharts();
  initTable();
  initChangelog();
  initNavigation();
  initExport();
  initTimeline();
  initModals();
  updateMetadata();
});
