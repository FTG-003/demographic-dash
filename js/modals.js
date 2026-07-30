/**
 * js/modals.js — Gestione finestre modali, focus management WCAG AA
 * Italian Demographic Observatory v1.4+
 */

function initModals() {
  var modal = getEl('infoModal');
  var lastFocus = null;

  document
    .querySelectorAll('.nav-btn[data-action="info"]')
    .forEach(function (btn) {
      if (!btn) return;
      btn.addEventListener('click', function () {
        lastFocus = document.activeElement;
        modal.classList.add('open');
        // Focus trap: sposta focus sul primo elemento focusable
        var closeBtn = getEl('closeInfoModal');
        if (closeBtn) closeBtn.focus();
      });
    });

  function close() {
    modal.classList.remove('open');
    if (lastFocus) {
      lastFocus.focus();
      lastFocus = null;
    }
  }

  var closeBtn1 = getEl('closeInfoModal');
  if (closeBtn1) closeBtn1.addEventListener('click', close);
  var closeBtn2 = getEl('closeInfoModalBtn');
  if (closeBtn2) closeBtn2.addEventListener('click', close);

  if (modal) {
    modal.addEventListener('click', function (e) {
      if (e.target === modal) close();
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal.classList.contains('open')) {
      close();
    }
    // Focus trap all'interno della modale
    if (e.key === 'Tab' && modal.classList.contains('open')) {
      var focusable = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (focusable.length === 0) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });
}
