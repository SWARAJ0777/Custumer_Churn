/* =========================================================================
   data.js
   Static sample dataset for the customer risk table.
   In a real deployment this would be fetched from a backend / API
   (e.g. GET /api/customers) — kept local here so the demo runs
   entirely client-side with zero dependencies.
   ========================================================================= */

const CUSTOMERS = [
  { name: 'Arjun Sharma',  id: 'CUS-2841', tenure: 8,  charges: 89,  contract: 'Month-to-Month', risk: 82, level: 'high',   action: 'Offer discount' },
  { name: 'Priya Patel',   id: 'CUS-1203', tenure: 3,  charges: 105, contract: 'Month-to-Month', risk: 91, level: 'high',   action: 'Retention call' },
  { name: 'Rahul Mehta',   id: 'CUS-0952', tenure: 24, charges: 65,  contract: 'One Year',       risk: 23, level: 'low',    action: 'Upsell bundle' },
  { name: 'Sneha Gupta',   id: 'CUS-3347', tenure: 6,  charges: 78,  contract: 'Month-to-Month', risk: 67, level: 'medium', action: 'Send offer' },
  { name: 'Vikram Nair',   id: 'CUS-0711', tenure: 48, charges: 45,  contract: 'Two Year',       risk: 7,  level: 'low',    action: 'Reward loyalty' },
  { name: 'Anjali Singh',  id: 'CUS-4420', tenure: 12, charges: 92,  contract: 'Month-to-Month', risk: 74, level: 'high',   action: 'Manager callback' },
  { name: 'Deepak Kumar',  id: 'CUS-2236', tenure: 36, charges: 58,  contract: 'One Year',       risk: 18, level: 'low',    action: 'Cross-sell' },
  { name: 'Kavya Reddy',   id: 'CUS-0504', tenure: 5,  charges: 112, contract: 'Month-to-Month', risk: 88, level: 'high',   action: 'Emergency intervention' },
  { name: 'Manish Iyer',   id: 'CUS-1987', tenure: 18, charges: 73,  contract: 'One Year',       risk: 38, level: 'medium', action: 'Value email' },
  { name: 'Sunita Joshi',  id: 'CUS-3312', tenure: 60, charges: 39,  contract: 'Two Year',       risk: 4,  level: 'low',    action: 'Referral invite' }
];

/* Monthly / quarterly churn trend series shared by the analytics chart */
const CHURN_TRENDS = {
  monthly: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    actual:    [8.2, 7.8, 7.1, 6.9, 6.4, 6.1, 5.9, 5.8, 5.6, 5.4, 5.2, 5.1],
    predicted: [8.0, 7.6, 7.2, 7.0, 6.5, 6.2, 5.8, 5.6, 5.5, 5.3, 5.1, 4.9]
  },
  quarterly: {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    actual:    [7.5, 6.5, 5.7, 5.1],
    predicted: [7.3, 6.4, 5.6, 5.0]
  }
};

/* Risk distribution for the doughnut chart */
const RISK_DISTRIBUTION = {
  labels: ['Low Risk', 'Medium Risk', 'High Risk'],
  values: [68, 20, 12],
  colors: ['#22c55e', '#f59e0b', '#ef4444']
};

/* SHAP-style feature importance values for the bar chart */
const FEATURE_IMPORTANCE = {
  labels: ['Contract Type', 'Monthly Charges', 'Tenure', 'Tech Support', 'Internet Service', 'Payment Method', 'Support Tickets', 'Satisfaction Score'],
  values: [0.42, 0.38, 0.31, 0.28, 0.24, 0.19, 0.16, 0.12],
  colors: ['#ef4444', '#f59e0b', '#4f8ef7', '#22c55e', '#a855f7', '#14b8a6', '#f97316', '#64748b']
};
