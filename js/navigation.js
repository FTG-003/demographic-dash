/**
 * js/navigation.js — Gestione scroll fluido, sticky header e toast/export
 * Italian Demographic Observatory v1.4+
 */

function initNavigation() {
  var navBtns = document.querySelectorAll('.nav-btn[data-view]');
  var targets = {
    overview: getEl('kpiBirths'),
    analysis: getEl('mainChart'),
    regions: getEl('regionsChart'),
    europe: getEl('europeChart'),
    projections: getEl('projectionChart'),
  };

  navBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var view = btn.getAttribute('data-view');
      navBtns.forEach(function (b) {
        b.classList.remove('active');
        b.removeAttribute('aria-current');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-current', 'page');

      var target = targets[view];
      if (target) {
        var header = document.querySelector('.observatory-console');
        var offset = header ? header.offsetHeight + 30 : 100;
        var top =
          target.getBoundingClientRect().top +
          window.pageYOffset -
          offset;
        window.scrollTo({ behavior: 'smooth', top: top });
      }
    });
  });
}

function initExport() {
  document
    .querySelectorAll('.nav-btn[data-action="export"]')
    .forEach(function (btn) {
      btn.addEventListener('click', function () {
        var chartIds = [
          { id: 'mainChart', name: 'evoluzione_demografica' },
          { id: 'europeChart', name: 'confronto_europeo' },
          { id: 'regionsChart', name: 'tfr_regionale' },
          { id: 'ageChart', name: 'struttura_eta' },
          { id: 'projectionChart', name: 'proiezioni' },
          { id: 'causesChart', name: 'fattori_declino' },
        ];
        showToast(
          'Esportazione di ' + chartIds.length + ' grafici in corso. Attendere...'
        );
        function doExport(i) {
          if (i >= chartIds.length) {
            showToast(
              'Esportazione completata: ' + chartIds.length + ' grafici.'
            );
            return;
          }
          downloadChart(chartIds[i].id, chartIds[i].name);
          setTimeout(function () {
            doExport(i + 1);
          }, 500);
        }
        doExport(0);
      });
    });
}
