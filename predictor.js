/* =========================================================================
   predictor.js
   Client-side "mock" churn prediction engine for the live demo form.
   Computes a heuristic risk score (0-100) from the entered customer
   attributes, derives contributing factors, and renders the result panel.

   NOTE: This is a rule-based simulation built for demonstration purposes
   (no server / real model is called). It mirrors the kind of feature
   weighting a trained XGBoost model would learn, so the UI/UX experience
   matches a production prediction API.
   ========================================================================= */

/**
 * Updates the visible satisfaction score value next to the range slider.
 * @param {string|number} value
 */
function updateSat(value) {
  const el = document.getElementById('sat_val');
  if (el) el.textContent = value;
  const slider = document.getElementById('f_sat');
  if (slider) slider.setAttribute('aria-valuenow', value);
}

/**
 * Reads all form inputs and returns a structured customer profile object.
 */
function readCustomerForm() {
  return {
    tenure: Number(document.getElementById('f_tenure').value) || 0,
    charges: Number(document.getElementById('f_charges').value) || 0,
    contract: document.getElementById('f_contract').value,
    internet: document.getElementById('f_internet').value,
    payment: document.getElementById('f_payment').value,
    tickets: Number(document.getElementById('f_tickets').value) || 0,
    techSupport: document.getElementById('f_techsupport').value,
    satisfaction: Number(document.getElementById('f_sat').value) || 3
  };
}

/**
 * Computes a heuristic churn risk score (0-100) from a customer profile.
 * @param {object} profile
 * @returns {number}
 */
function computeChurnScore(profile) {
  let score = 0;

  // Contract type is the strongest signal
  if (profile.contract === 'month') score += 30;
  else if (profile.contract === 'year') score += 8;
  else score += 2;

  // Pricing pressure
  if (profile.charges > 80) score += 20;
  else if (profile.charges > 60) score += 10;

  // Tenure / loyalty
  if (profile.tenure < 12) score += 20;
  else if (profile.tenure < 24) score += 10;
  else score -= 10;

  // Service type
  if (profile.internet === 'Fiber Optic') score += 8;

  // Payment friction
  if (profile.payment === 'Electronic Check') score += 10;

  // Support burden
  if (profile.tickets >= 3) score += profile.tickets * 4;

  // Lack of retention-boosting add-ons
  if (profile.techSupport === 'No') score += 8;

  // Satisfaction (inverse relationship)
  score += (5 - profile.satisfaction) * 6;

  // Small random jitter so repeated identical inputs feel "live"
  score += Math.random() * 6 - 3;

  return Math.min(98, Math.max(3, Math.round(score)));
}

/**
 * Derives the top contributing risk factors for display, sorted by impact.
 * @param {object} profile
 * @returns {Array<{label: string, impact: number, color: string}>}
 */
function deriveRiskFactors(profile) {
  const factors = [];

  if (profile.contract === 'month') {
    factors.push({ label: 'Month-to-Month Contract', impact: 0.85, color: '#ef4444' });
  }
  if (profile.charges > 80) {
    factors.push({ label: `High Monthly Charges ($${profile.charges})`, impact: 0.72, color: '#f59e0b' });
  }
  if (profile.tenure < 12) {
    factors.push({ label: `Short Tenure (${profile.tenure} months)`, impact: 0.65, color: '#f59e0b' });
  }
  if (profile.tickets >= 3) {
    factors.push({ label: `${profile.tickets} Support Tickets`, impact: 0.55, color: '#a855f7' });
  }
  if (profile.techSupport === 'No') {
    factors.push({ label: 'No Tech Support', impact: 0.40, color: '#4f8ef7' });
  }
  if (profile.satisfaction <= 2) {
    factors.push({ label: `Low Satisfaction (${profile.satisfaction}/5)`, impact: 0.60, color: '#ef4444' });
  }

  // Sort strongest impact first, return top 4
  return factors.sort((a, b) => b.impact - a.impact).slice(0, 4);
}

/**
 * Derives recommended retention actions based on the customer profile.
 * @param {object} profile
 * @returns {Array<{text: string, cls: string}>}
 */
function deriveActions(profile) {
  const actions = [];

  if (profile.contract === 'month') {
    actions.push({ text: 'Offer annual contract discount', cls: 'pill-green' });
  }
  if (profile.charges > 80) {
    actions.push({ text: 'Bundle value-add services', cls: 'pill-blue' });
  }
  if (profile.tickets >= 3) {
    actions.push({ text: 'Priority support escalation', cls: 'pill-amber' });
  }
  if (profile.satisfaction <= 2) {
    actions.push({ text: 'Customer success call', cls: 'pill-green' });
  }
  if (profile.tenure < 12) {
    actions.push({ text: 'Onboarding review session', cls: 'pill-blue' });
  }
  if (actions.length === 0) {
    actions.push({ text: 'Quarterly check-in', cls: 'pill-blue' });
  }

  return actions;
}

/**
 * Maps a numeric score to a risk badge label + CSS class.
 * @param {number} score
 */
function getRiskBand(score) {
  if (score >= 60) return { label: 'High Risk', cls: 'risk-high', color: '#ef4444' };
  if (score >= 30) return { label: 'Medium Risk', cls: 'risk-med', color: '#f59e0b' };
  return { label: 'Low Risk', cls: 'risk-low', color: '#22c55e' };
}

/**
 * Renders the prediction result into the result panel DOM.
 * @param {number} score
 * @param {Array} factors
 * @param {Array} actions
 */
function renderPredictionResult(score, factors, actions) {
  const placeholder = document.getElementById('result_placeholder');
  const content = document.getElementById('result_content');

  placeholder.style.display = 'none';
  content.hidden = false;

  // Percentage + colour
  const band = getRiskBand(score);
  const pctEl = document.getElementById('r_pct');
  pctEl.textContent = score + '%';
  pctEl.style.color = band.color;

  // Badge
  const badgeEl = document.getElementById('r_badge');
  badgeEl.textContent = band.label;
  badgeEl.className = 'risk-badge ' + band.cls;

  // Indicator position on the gradient bar
  document.getElementById('r_indicator').style.left = score + '%';

  // Risk factors
  const factorList = document.getElementById('r_factors');
  factorList.innerHTML = '';
  if (factors.length === 0) {
    factorList.innerHTML = '<li style="font-size:13px;color:var(--text3);text-align:center;padding:8px;">No significant risk factors detected</li>';
  } else {
    factors.forEach((f) => {
      const li = document.createElement('li');
      li.className = 'factor-item';
      li.innerHTML = `
        <span>${f.label}</span>
        <div class="impact-bar-wrap">
          <div class="impact-bar" style="width:${Math.round(f.impact * 100)}%;background:${f.color};"></div>
        </div>
        <span class="factor-impact" style="color:${f.color};">${f.impact.toFixed(2)}</span>
      `;
      factorList.appendChild(li);
    });
  }

  // Recommended actions
  const actionsWrap = document.getElementById('r_actions');
  actionsWrap.innerHTML = actions
    .map((a) => `<span class="action-pill ${a.cls}">${a.text}</span>`)
    .join('');

  // Confidence note
  const confidence = Math.round(91 + Math.random() * 6);
  document.getElementById('r_confidence').textContent = confidence + '%';
}

/**
 * Main entry point — triggered by the "Predict Churn Probability" button.
 * Reads the form, computes the score, and renders the result.
 */
function runPrediction() {
  const btn = document.getElementById('predict-btn');
  const profile = readCustomerForm();

  // Brief loading state for perceived responsiveness
  btn.classList.add('is-loading');
  const originalLabel = btn.innerHTML;
  btn.innerHTML = '<i class="ti ti-loader-2"></i> Analyzing…';

  setTimeout(() => {
    const score = computeChurnScore(profile);
    const factors = deriveRiskFactors(profile);
    const actions = deriveActions(profile);

    renderPredictionResult(score, factors, actions);

    btn.classList.remove('is-loading');
    btn.innerHTML = originalLabel;
  }, 450); // simulated inference latency
}
