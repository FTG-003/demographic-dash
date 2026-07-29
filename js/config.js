/**
 * js/config.js — Metadati, configurazione colori/gradienti semantici
 * e funzioni utility di formattazione numeri/date.
 * Italian Demographic Observatory v1.4+
 */

/* ── Funzioni utility globali ── */

/** shorthand per document.getElementById */
function getEl(id) {
  return document.getElementById(id);
}

/**
 * Formatta un numero in locale italiano (es. 370000 → "370.000")
 * @param {number} n
 * @param {number} [decimals=0]
 * @returns {string}
 */
function formatNum(n, decimals) {
  if (decimals === undefined) decimals = 0;
  return n.toLocaleString('it-IT', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

/**
 * Mostra un toast notification per 3 secondi
 * @param {string} msg
 */
function showToast(msg) {
  var toast = getEl('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._hideTimer);
  toast._hideTimer = setTimeout(function () {
    toast.classList.remove('show');
  }, 3000);
}

/**
 * Scarica un canvas come PNG
 * @param {string} canvasId
 * @param {string} filename
 */
function downloadChart(canvasId, filename) {
  var canvas = getEl(canvasId);
  if (!canvas) return;
  try {
    var url = canvas.toDataURL('image/png');
    var link = document.createElement('a');
    link.download =
      (filename || 'chart') + '_v' + DATA.metadata.dataset_version + '.png';
    link.href = url;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Grafico scaricato: ' + link.download);
  } catch (e) {
    showToast('Errore durante il download del grafico.');
  }
}

/* ── Configurazione gradienti semantici ── */

/**
 * Crea un gradiente lineare verticale per un contest canvas.
 * @param {CanvasRenderingContext2D} ctx
 * @param {number} height - altezza del gradiente
 * @param {string} color - colore base in formato 'rgba(r,g,b,a)'
 * @returns {CanvasGradient}
 */
function createVerticalGradient(ctx, height, color) {
  var g = ctx.createLinearGradient(0, 0, 0, height || 400);
  g.addColorStop(0, color.replace('1)', '0.25)'));
  g.addColorStop(1, color.replace('1)', '0.0)'));
  return g;
}

/* ── Colori e gradienti per i vari grafici ── */
const COLORS = {
  // Main chart dataset colors
  births: '#10B981',
  deaths: '#DC2626',
  tfr: '#3B82F6',
  // Europe / Regions threshold colors
  violet: 'rgba(127,0,255,0.85)',
  magenta: 'rgba(225,0,255,0.7)',
  magentaDim: 'rgba(225,0,255,0.45)',
  violetBorder: '#7F00FF',
  magentaBorder: '#E100FF',
  magentaBorderDim: 'rgba(225,0,255,0.6)',
  // Age structure
  ageColors: [
    'rgba(0,242,254,0.7)',
    'rgba(79,172,254,0.7)',
    'rgba(37,117,252,0.7)',
    'rgba(107,72,255,0.7)',
    'rgba(127,0,255,0.7)',
  ],
  // Projections
  projOptimistic: 'rgba(0,242,254,0.6)',
  projBase: '#00F2FE',
  projPessimistic: 'rgba(79,172,254,0.6)',
  // Causes chart (radar)
  radarBorder: '#FFB75E',
  radarFill: 'rgba(255,183,94,0.15)',
  radarPoint: '#FFB75E',
};

/**
 * Restituisce il colore di sfondo per una barra in base al valore
 * rispetto a soglie predefinite.
 */
function barColor(value, highThreshold, midThreshold) {
  if (value >= highThreshold) return COLORS.violet;
  if (value >= midThreshold) return COLORS.magenta;
  return COLORS.magentaDim;
}

function barBorder(value, highThreshold, midThreshold) {
  if (value >= highThreshold) return COLORS.violetBorder;
  if (value >= midThreshold) return COLORS.magentaBorder;
  return COLORS.magentaBorderDim;
}
