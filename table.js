/* =========================================================================
   table.js
   Renders the customer risk table, and powers live search + risk-level
   filtering using the CUSTOMERS dataset defined in data.js.
   ========================================================================= */

let currentTableFilter = 'all';

/**
 * Returns the hex colour + readable label for a given risk level.
 * @param {'high'|'medium'|'low'} level
 */
function getRiskMeta(level) {
  switch (level) {
    case 'high':
      return { color: '#ef4444', bg: 'rgba(239,68,68,.12)', label: 'High' };
    case 'medium':
      return { color: '#f59e0b', bg: 'rgba(245,158,11,.12)', label: 'Medium' };
    default:
      return { color: '#22c55e', bg: 'rgba(34,197,94,.12)', label: 'Low' };
  }
}

/**
 * Renders a list of customer records into the table body.
 * @param {Array} list - filtered/sorted subset of CUSTOMERS
 */
function renderTable(list) {
  const tbody = document.getElementById('customer_table_body');

  if (!list.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="table-empty">No customers match your search or filter.</td></tr>`;
    return;
  }

  tbody.innerHTML = list
    .map((c) => {
      const meta = getRiskMeta(c.level);
      return `
        <tr>
          <td>
            <div class="cust-name">${c.name}</div>
            <div class="cust-id">${c.id}</div>
          </td>
          <td>${c.tenure} mo</td>
          <td>$${c.charges}</td>
          <td style="font-size:12px;">${c.contract}</td>
          <td>
            <div class="churn-pct">
              <div class="churn-mini-bar">
                <div class="churn-mini-fill" style="width:${c.risk}%;background:${meta.color};"></div>
              </div>
              <span style="color:${meta.color};font-weight:600;">${c.risk}%</span>
            </div>
          </td>
          <td><span class="status-pill" style="background:${meta.bg};color:${meta.color};">${meta.label}</span></td>
          <td><span style="font-size:12px;color:var(--text2);">${c.action}</span></td>
        </tr>
      `;
    })
    .join('');
}

/**
 * Applies the current search query and risk filter together,
 * then re-renders the table.
 */
function filterTable() {
  const query = document.getElementById('tableSearch').value.trim().toLowerCase();

  let list = CUSTOMERS.filter(
    (c) => currentTableFilter === 'all' || c.level === currentTableFilter
  );

  if (query) {
    list = list.filter(
      (c) =>
        c.name.toLowerCase().includes(query) ||
        c.id.toLowerCase().includes(query)
    );
  }

  renderTable(list);
}

/**
 * Sets the active risk-level filter and re-applies filtering.
 * Called from the inline onclick on each filter button.
 * @param {'all'|'high'|'medium'|'low'} level
 */
function filterRisk(level) {
  currentTableFilter = level;

  document.querySelectorAll('.filter-btn').forEach((btn) => {
    btn.classList.remove('active-filter');
  });
  document.getElementById('filter_' + level).classList.add('active-filter');

  filterTable();
}
