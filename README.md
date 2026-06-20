# ChurnGuard — Customer Churn Prediction (Portfolio Project)

A fully responsive, production-styled front-end for a customer churn
prediction platform. Built with plain HTML5, CSS3, and vanilla ES6+
JavaScript — no build step, no frameworks, no dependencies to install.

## ✨ Features

- **Hero dashboard** with animated SVG risk gauge and floating insight cards
- **Live KPI metrics** (accuracy, revenue saved, at-risk customers, etc.)
- **Interactive analytics charts** (Chart.js): churn trend line chart with
  monthly/quarterly toggle, risk distribution doughnut, SHAP feature
  importance bar chart
- **Live churn predictor** — fill in a customer profile and get an instant
  heuristic risk score, contributing factors, and recommended retention
  actions
- **Customer risk segments** with animated progress bars (IntersectionObserver)
- **Model insight cards** explaining key churn drivers
- **Interactive ML pipeline walkthrough** with syntax-highlighted code
  snippets for each stage (ingestion → feature engineering → training →
  evaluation → deployment)
- **Searchable / filterable customer table**
- **Tech stack showcase** and contact/CTA section
- Fully responsive (desktop, tablet, mobile) with a mobile hamburger nav
- Scroll-spy navigation, smooth scrolling, reduced-motion support

## 📁 Project Structure

```
churnguard/
├── index.html              # Main HTML document (all sections/markup)
├── README.md                # This file
├── css/
│   └── style.css            # All styling: variables, layout, components,
│                             # animations, responsive breakpoints
└── js/
    ├── data.js               # Static sample dataset (customers, chart data)
    ├── charts.js              # Chart.js setup (line / doughnut / bar charts)
    ├── predictor.js           # Live churn prediction scoring engine
    ├── pipeline.js             # Pipeline step switcher + code snippets
    ├── table.js                # Customer table render/search/filter
    └── main.js                  # App bootstrap: nav, scroll-spy, init calls
```

## 🚀 Running Locally

No build tools or installation required.

1. Download/clone the `churnguard` folder.
2. Open `index.html` directly in any modern browser, **or** serve it with
   a simple local server (recommended, avoids any `file://` CORS quirks):

   ```bash
   # Python 3
   cd churnguard
   python3 -m http.server 8000
   # then visit http://localhost:8000
   ```

   ```bash
   # Node (npx, no install)
   npx serve churnguard
   ```

That's it — the app is 100% static and runs entirely client-side.

## 🌐 External Dependencies (via CDN)

These are loaded directly in `index.html` — no npm install needed:

| Library | Purpose | Source |
|---|---|---|
| Google Fonts — Inter & JetBrains Mono | Typography | fonts.googleapis.com |
| Tabler Icons (webfont) | UI icons | cdn.jsdelivr.net |
| Chart.js 4.4.1 | Analytics charts | cdnjs.cloudflare.com |

If you need a fully offline build, download these three assets locally and
update the `<link>`/`<script>` paths in `index.html` accordingly.

## 🎨 Customization Guide

- **Colors / theme** — all design tokens live at the top of `css/style.css`
  inside `:root { ... }`. Change `--accent`, `--bg`, gradients, etc. to
  re-theme the whole site instantly.
- **Customer data** — edit the `CUSTOMERS` array in `js/data.js` to swap in
  your own sample records (or wire it up to a real API).
- **Chart data** — `CHURN_TRENDS`, `RISK_DISTRIBUTION`, and
  `FEATURE_IMPORTANCE` in `js/data.js` feed the three analytics charts.
- **Prediction logic** — `js/predictor.js` contains a transparent, fully
  commented heuristic scoring function (`computeChurnScore`). Replace this
  with a real `fetch()` call to your backend / ML API for a production
  deployment (e.g. a FastAPI endpoint as shown in the Pipeline section's
  code sample).
- **Pipeline code snippets** — edit `PIPELINE_CONTENT` in `js/pipeline.js`
  to update the syntax-highlighted code shown for each ML pipeline stage.

## ♿ Accessibility

- Semantic landmarks (`nav`, `section`, `footer`) and heading hierarchy
- ARIA labels/roles on charts, progress bars, gauges, and live regions
- Visible focus states (`:focus-visible`) on all interactive elements
- `prefers-reduced-motion` support disables animations for users who
  request it

## 📱 Responsive Breakpoints

| Breakpoint | Behavior |
|---|---|
| `> 1024px` | Full multi-column desktop layout |
| `≤ 1024px` | Metrics/tech grids collapse to 2 columns, charts stack |
| `≤ 900px`  | Hero/predictor/pipeline collapse to 1 column, mobile nav appears |
| `≤ 640px`  | Single-column forms/grids, compact spacing, stacked footer |

## 📄 License

Free to use and modify for personal portfolio purposes.
