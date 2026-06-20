/* =========================================================================
   charts.js
   Initialises and controls all Chart.js visualisations:
     1. Churn rate line chart (monthly / quarterly toggle)
     2. Risk distribution doughnut chart
     3. Feature importance (SHAP) horizontal bar chart
   ========================================================================= */

let churnChartInstance = null;

/**
 * Builds the line chart used for "Churn Rate Over Time".
 */
function initChurnChart() {
  const canvas = document.getElementById('churnChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const { labels, actual, predicted } = CHURN_TRENDS.monthly;
  const retention = actual.map((v) => +(100 - v).toFixed(1));

  churnChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Churn Rate',
          data: actual,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239,68,68,.08)',
          fill: true,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: '#ef4444'
        },
        {
          label: 'Predicted',
          data: predicted,
          borderColor: '#4f8ef7',
          borderDash: [4, 4],
          fill: false,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 0
        },
        {
          label: 'Retention',
          data: retention,
          borderColor: '#22c55e',
          fill: false,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,.04)' },
          ticks: { color: '#5a6a8a', font: { size: 11 } }
        },
        y: {
          grid: { color: 'rgba(255,255,255,.04)' },
          ticks: {
            color: '#5a6a8a',
            font: { size: 11 },
            callback: (v) => v + '%'
          }
        }
      }
    }
  });
}

/**
 * Toggles the churn chart between monthly and quarterly data.
 * Called from the inline onclick on the chart-tab buttons.
 * @param {HTMLElement} btn - the tab button that was clicked
 * @param {'monthly'|'quarterly'} period
 */
function switchChart(btn, period) {
  document.querySelectorAll('.chart-tab').forEach((tab) => {
    tab.classList.remove('active');
    tab.setAttribute('aria-selected', 'false');
  });
  btn.classList.add('active');
  btn.setAttribute('aria-selected', 'true');

  if (!churnChartInstance) return;
  const { labels, actual, predicted } = CHURN_TRENDS[period];
  const retention = actual.map((v) => +(100 - v).toFixed(1));

  churnChartInstance.data.labels = labels;
  churnChartInstance.data.datasets[0].data = actual;
  churnChartInstance.data.datasets[1].data = predicted;
  churnChartInstance.data.datasets[2].data = retention;
  churnChartInstance.update();
}

/**
 * Builds the doughnut chart used for "Risk Distribution".
 */
function initRiskChart() {
  const canvas = document.getElementById('riskChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: RISK_DISTRIBUTION.labels,
      datasets: [
        {
          data: RISK_DISTRIBUTION.values,
          backgroundColor: RISK_DISTRIBUTION.colors,
          borderWidth: 0,
          hoverOffset: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '72%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.label}: ${ctx.parsed}%`
          }
        }
      }
    }
  });
}

/**
 * Builds the horizontal bar chart used for "Feature Importance (SHAP Values)".
 */
function initFeatureChart() {
  const canvas = document.getElementById('featureChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: FEATURE_IMPORTANCE.labels,
      datasets: [
        {
          label: 'SHAP Value',
          data: FEATURE_IMPORTANCE.values,
          backgroundColor: FEATURE_IMPORTANCE.colors,
          borderRadius: 4
        }
      ]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,.04)' },
          ticks: { color: '#5a6a8a', font: { size: 11 } }
        },
        y: {
          grid: { display: false },
          ticks: { color: '#94a3c4', font: { size: 12 } }
        }
      }
    }
  });
}

/**
 * Initialises all charts. Called once on DOMContentLoaded from main.js.
 */
function initAllCharts() {
  initChurnChart();
  initRiskChart();
  initFeatureChart();
}
