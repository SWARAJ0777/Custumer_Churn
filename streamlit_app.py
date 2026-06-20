"""
ChurnGuard — Customer Churn Prediction Dashboard
==================================================
A Streamlit recreation of the ChurnGuard portfolio web app: a dark,
modern, ML-styled dashboard for customer churn prediction featuring
live scoring, analytics charts, customer segmentation, an ML pipeline
walkthrough, and a searchable customer risk table.

Run locally:
    pip install -r requirements.txt
    streamlit run streamlit_app.py

Deploy:
    Push this repo to GitHub and deploy on https://share.streamlit.io
    (Streamlit Community Cloud). Entry point: streamlit_app.py
"""

import time
import random

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# =============================================================================
# PAGE CONFIG  (must be the first Streamlit call)
# =============================================================================
st.set_page_config(
    page_title="ChurnGuard — Customer Churn Prediction",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# DESIGN TOKENS — mirrors the original ChurnGuard CSS variables
# =============================================================================
COLORS = {
    "bg": "#0a0e1a",
    "bg2": "#111827",
    "bg3": "#1a2236",
    "card": "#131b2e",
    "card2": "#1a2440",
    "border": "#2a3555",
    "text": "#e8edf8",
    "text2": "#94a3c4",
    "text3": "#5a6a8a",
    "accent": "#4f8ef7",
    "accent2": "#6ba3f8",
    "green": "#22c55e",
    "red": "#ef4444",
    "amber": "#f59e0b",
    "purple": "#a855f7",
    "teal": "#14b8a6",
}

# =============================================================================
# GLOBAL CSS — dark theme styling to match the ChurnGuard web design
# =============================================================================
def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}

        .stApp {{
            background: {COLORS['bg']};
            color: {COLORS['text']};
        }}

        /* Hide default Streamlit chrome for a cleaner portfolio look */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{
            background: transparent;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background: {COLORS['bg2']};
            border-right: 1px solid {COLORS['border']};
        }}
        section[data-testid="stSidebar"] * {{
            color: {COLORS['text']} !important;
        }}

        /* Headings */
        h1, h2, h3, h4 {{
            color: {COLORS['text']} !important;
            font-weight: 700 !important;
        }}

        /* Hero badge */
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(79, 142, 247, 0.12);
            border: 1px solid rgba(79, 142, 247, 0.3);
            color: {COLORS['accent2']};
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 14px;
        }}
        .badge-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: {COLORS['accent']};
            display: inline-block;
        }}

        .gradient-text {{
            background: linear-gradient(135deg, #4f8ef7 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .section-eyebrow {{
            font-size: 12px;
            font-weight: 700;
            color: {COLORS['accent']};
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 6px;
        }}

        .section-sub {{
            font-size: 15px;
            color: {COLORS['text2']};
            max-width: 640px;
            line-height: 1.6;
            margin-bottom: 8px;
        }}

        /* Generic card */
        .cg-card {{
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 22px;
        }}

        /* Metric cards (custom, on top of native st.metric) */
        .metric-card {{
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }}
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
        }}
        .metric-card.blue::before {{ background: linear-gradient(135deg,#4f8ef7,#a855f7); }}
        .metric-card.green::before {{ background: linear-gradient(135deg,#22c55e,#14b8a6); }}
        .metric-card.amber::before {{ background: linear-gradient(135deg,#f59e0b,#ef4444); }}
        .metric-card.purple::before {{ background: linear-gradient(135deg,#a855f7,#ec4899); }}
        .metric-icon {{
            width: 38px; height: 38px;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 18px;
            margin-bottom: 12px;
        }}
        .metric-num {{ font-size: 28px; font-weight: 700; margin-bottom: 2px; }}
        .metric-label {{ font-size: 13px; color: {COLORS['text2']}; margin-bottom: 6px; }}
        .metric-trend {{ font-size: 12px; }}
        .trend-up {{ color: {COLORS['green']}; }}
        .trend-down {{ color: {COLORS['red']}; }}

        /* Risk badge pills */
        .risk-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
        }}
        .risk-high {{ background: rgba(239,68,68,.15); color: #f87171; }}
        .risk-med  {{ background: rgba(245,158,11,.15); color: #fbbf24; }}
        .risk-low  {{ background: rgba(34,197,94,.15);  color: #4ade80; }}

        /* Factor / action pills */
        .factor-item {{
            display: flex; align-items: center; justify-content: space-between;
            background: {COLORS['bg3']};
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 13px;
            margin-bottom: 8px;
        }}
        .action-pill {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid;
            margin: 3px 4px 3px 0;
        }}
        .pill-green {{ background: rgba(34,197,94,.1);  border-color: rgba(34,197,94,.3);  color: #4ade80; }}
        .pill-blue  {{ background: rgba(79,142,247,.1); border-color: rgba(79,142,247,.3); color: {COLORS['accent2']}; }}
        .pill-amber {{ background: rgba(245,158,11,.1); border-color: rgba(245,158,11,.3); color: #fbbf24; }}

        /* Segment cards */
        .segment-card {{
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 20px;
        }}
        .segment-icon {{
            width: 42px; height: 42px;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px;
            margin-bottom: 10px;
        }}

        /* Insight cards */
        .insight-card {{
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 20px;
            height: 100%;
        }}

        /* Pipeline */
        .pipeline-step-label {{
            font-size: 14px;
            font-weight: 600;
            color: {COLORS['text']};
        }}
        .pipeline-step-desc {{
            font-size: 12px;
            color: {COLORS['text2']};
        }}
        .code-wrap {{
            background: {COLORS['bg']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 4px;
        }}

        hr {{
            border-color: {COLORS['border']} !important;
        }}

        /* Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, #4f8ef7 0%, #a855f7 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover {{
            opacity: 0.9;
            transform: translateY(-1px);
        }}

        /* Inputs */
        .stSelectbox > div > div, .stNumberInput > div > div input {{
            background: {COLORS['bg3']} !important;
            border: 1px solid {COLORS['border']} !important;
            color: {COLORS['text']} !important;
        }}

        /* DataFrame */
        [data-testid="stDataFrame"] {{
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# SAMPLE DATA  — mirrors data.js from the original web project
# =============================================================================
@st.cache_data
def load_customers() -> pd.DataFrame:
    rows = [
        ("Arjun Sharma", "CUS-2841", 8, 89, "Month-to-Month", 82, "High", "Offer discount"),
        ("Priya Patel", "CUS-1203", 3, 105, "Month-to-Month", 91, "High", "Retention call"),
        ("Rahul Mehta", "CUS-0952", 24, 65, "One Year", 23, "Low", "Upsell bundle"),
        ("Sneha Gupta", "CUS-3347", 6, 78, "Month-to-Month", 67, "Medium", "Send offer"),
        ("Vikram Nair", "CUS-0711", 48, 45, "Two Year", 7, "Low", "Reward loyalty"),
        ("Anjali Singh", "CUS-4420", 12, 92, "Month-to-Month", 74, "High", "Manager callback"),
        ("Deepak Kumar", "CUS-2236", 36, 58, "One Year", 18, "Low", "Cross-sell"),
        ("Kavya Reddy", "CUS-0504", 5, 112, "Month-to-Month", 88, "High", "Emergency intervention"),
        ("Manish Iyer", "CUS-1987", 18, 73, "One Year", 38, "Medium", "Value email"),
        ("Sunita Joshi", "CUS-3312", 60, 39, "Two Year", 4, "Low", "Referral invite"),
    ]
    return pd.DataFrame(
        rows,
        columns=["Customer", "ID", "Tenure (mo)", "Monthly $", "Contract", "Churn Risk %", "Risk Level", "Recommended Action"],
    )


CHURN_TRENDS = {
    "Monthly": {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "actual": [8.2, 7.8, 7.1, 6.9, 6.4, 6.1, 5.9, 5.8, 5.6, 5.4, 5.2, 5.1],
        "predicted": [8.0, 7.6, 7.2, 7.0, 6.5, 6.2, 5.8, 5.6, 5.5, 5.3, 5.1, 4.9],
    },
    "Quarterly": {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "actual": [7.5, 6.5, 5.7, 5.1],
        "predicted": [7.3, 6.4, 5.6, 5.0],
    },
}

RISK_DISTRIBUTION = {"labels": ["Low Risk", "Medium Risk", "High Risk"], "values": [68, 20, 12],
                      "colors": [COLORS["green"], COLORS["amber"], COLORS["red"]]}

FEATURE_IMPORTANCE = {
    "labels": ["Contract Type", "Monthly Charges", "Tenure", "Tech Support",
               "Internet Service", "Payment Method", "Support Tickets", "Satisfaction Score"],
    "values": [0.42, 0.38, 0.31, 0.28, 0.24, 0.19, 0.16, 0.12],
    "colors": ["#ef4444", "#f59e0b", "#4f8ef7", "#22c55e", "#a855f7", "#14b8a6", "#f97316", "#64748b"],
}

PIPELINE_STEPS = [
    {
        "title": "Data Ingestion",
        "sub": "ETL from CRM, billing, support systems",
        "icon": "🗄️",
        "code": """import pandas as pd
from sqlalchemy import create_engine

# Connect to data sources
engine = create_engine('postgresql://...')
crm_df = pd.read_sql('SELECT * FROM customers', engine)
billing_df = pd.read_sql('SELECT * FROM billing', engine)

# Merge datasets
df = crm_df.merge(billing_df, on='customer_id')
print(f"Loaded {len(df):,} records")
# Output: Loaded 50,000 records""",
    },
    {
        "title": "Feature Engineering",
        "sub": "38 derived features from raw signals",
        "icon": "🧪",
        "code": """def engineer_features(df):
    # Tenure buckets
    df['tenure_bin'] = pd.cut(df['tenure'], bins=[0,12,24,48,72])

    # Charge to tenure ratio
    df['charge_per_month'] = df['total_charges'] / (df['tenure']+1)

    # Interaction features
    df['no_support_high_charge'] = (
        (df['monthly_charges'] > 80) &
        (df['tech_support'] == 'No')
    ).astype(int)
    return df""",
    },
    {
        "title": "Model Training",
        "sub": "XGBoost + Random Forest ensemble",
        "icon": "🧠",
        "code": """import xgboost as xgb
from sklearn.model_selection import StratifiedKFold

# Define ensemble model
xgb_model = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    eval_metric='auc'
)

# 5-fold cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True)
scores = cross_val_score(xgb_model, X_train, y_train, cv=cv)
print(f"Mean AUC: {scores.mean():.4f}")
# Output: Mean AUC: 0.9421""",
    },
    {
        "title": "Evaluation & SHAP",
        "sub": "AUC-ROC, precision-recall, explainability",
        "icon": "🔬",
        "code": """import shap

# SHAP explainer
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test)

# Evaluate model
from sklearn.metrics import roc_auc_score
y_pred = xgb_model.predict_proba(X_test)[:,1]
auc = roc_auc_score(y_test, y_pred)
print(f"Test AUC: {auc:.4f}")
# Output: Test AUC: 0.9418""",
    },
    {
        "title": "Deployment & API",
        "sub": "FastAPI + Docker + real-time scoring",
        "icon": "🚀",
        "code": """from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ChurnGuard API")

class CustomerData(BaseModel):
    tenure: int
    monthly_charges: float
    contract: str
    tech_support: str

@app.post("/predict")
async def predict_churn(data: CustomerData):
    features = preprocess(data)
    prob = model.predict_proba(features)[0,1]
    return {"churn_probability": round(float(prob), 4)}""",
    },
]


# =============================================================================
# PREDICTION ENGINE — heuristic scoring (mirrors predictor.js logic)
# =============================================================================
def compute_churn_score(tenure, charges, contract, internet, payment, tickets, tech_support, satisfaction) -> int:
    """Rule-based churn score simulating a trained model's feature weighting."""
    score = 0.0

    if contract == "Month-to-Month":
        score += 30
    elif contract == "One Year":
        score += 8
    else:
        score += 2

    if charges > 80:
        score += 20
    elif charges > 60:
        score += 10

    if tenure < 12:
        score += 20
    elif tenure < 24:
        score += 10
    else:
        score -= 10

    if internet == "Fiber Optic":
        score += 8

    if payment == "Electronic Check":
        score += 10

    if tickets >= 3:
        score += tickets * 4

    if tech_support == "No":
        score += 8

    score += (5 - satisfaction) * 6
    score += random.uniform(-3, 3)

    return int(min(98, max(3, round(score))))


def derive_risk_factors(tenure, charges, contract, tickets, tech_support, satisfaction) -> list[dict]:
    factors = []
    if contract == "Month-to-Month":
        factors.append({"label": "Month-to-Month Contract", "impact": 0.85, "color": COLORS["red"]})
    if charges > 80:
        factors.append({"label": f"High Monthly Charges (${charges})", "impact": 0.72, "color": COLORS["amber"]})
    if tenure < 12:
        factors.append({"label": f"Short Tenure ({tenure} months)", "impact": 0.65, "color": COLORS["amber"]})
    if tickets >= 3:
        factors.append({"label": f"{tickets} Support Tickets", "impact": 0.55, "color": COLORS["purple"]})
    if tech_support == "No":
        factors.append({"label": "No Tech Support", "impact": 0.40, "color": COLORS["accent"]})
    if satisfaction <= 2:
        factors.append({"label": f"Low Satisfaction ({satisfaction}/5)", "impact": 0.60, "color": COLORS["red"]})
    factors.sort(key=lambda f: f["impact"], reverse=True)
    return factors[:4]


def derive_actions(tenure, charges, contract, tickets, satisfaction) -> list[dict]:
    actions = []
    if contract == "Month-to-Month":
        actions.append({"text": "Offer annual contract discount", "cls": "pill-green"})
    if charges > 80:
        actions.append({"text": "Bundle value-add services", "cls": "pill-blue"})
    if tickets >= 3:
        actions.append({"text": "Priority support escalation", "cls": "pill-amber"})
    if satisfaction <= 2:
        actions.append({"text": "Customer success call", "cls": "pill-green"})
    if tenure < 12:
        actions.append({"text": "Onboarding review session", "cls": "pill-blue"})
    if not actions:
        actions.append({"text": "Quarterly check-in", "cls": "pill-blue"})
    return actions


def risk_band(score: int) -> dict:
    if score >= 60:
        return {"label": "High Risk", "cls": "risk-high", "color": COLORS["red"]}
    if score >= 30:
        return {"label": "Medium Risk", "cls": "risk-med", "color": COLORS["amber"]}
    return {"label": "Low Risk", "cls": "risk-low", "color": COLORS["green"]}


# =============================================================================
# CHART BUILDERS — Plotly, dark-themed to match the design system
# =============================================================================
def base_layout(height: int = 320) -> dict:
    return dict(
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text2"], family="Inter", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    font=dict(color=COLORS["text2"])),
        xaxis=dict(gridcolor="rgba(255,255,255,.04)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,.04)", zeroline=False),
    )


def build_churn_trend_chart(period: str) -> go.Figure:
    data = CHURN_TRENDS[period]
    retention = [round(100 - v, 1) for v in data["actual"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["labels"], y=data["actual"], name="Churn Rate",
        mode="lines+markers", line=dict(color=COLORS["red"], width=2.5),
        marker=dict(size=6, color=COLORS["red"]),
        fill="tozeroy", fillcolor="rgba(239,68,68,0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=data["labels"], y=data["predicted"], name="Predicted",
        mode="lines", line=dict(color=COLORS["accent"], width=2, dash="dash"),
    ))
    fig.add_trace(go.Scatter(
        x=data["labels"], y=retention, name="Retention",
        mode="lines", line=dict(color=COLORS["green"], width=2),
    ))
    layout = base_layout(300)
    layout["yaxis"]["ticksuffix"] = "%"
    fig.update_layout(**layout)
    return fig


def build_risk_doughnut() -> go.Figure:
    fig = go.Figure(data=[go.Pie(
        labels=RISK_DISTRIBUTION["labels"],
        values=RISK_DISTRIBUTION["values"],
        hole=0.72,
        marker=dict(colors=RISK_DISTRIBUTION["colors"], line=dict(color=COLORS["bg"], width=2)),
        textinfo="none",
        hovertemplate="%{label}: %{value}%<extra></extra>",
    )])
    layout = base_layout(260)
    layout["showlegend"] = False
    fig.update_layout(**layout)
    return fig


def build_feature_importance_chart() -> go.Figure:
    labels = FEATURE_IMPORTANCE["labels"][::-1]
    values = FEATURE_IMPORTANCE["values"][::-1]
    colors = FEATURE_IMPORTANCE["colors"][::-1]

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=colors),
        text=[f"{v:.2f}" for v in values],
        textposition="outside",
        textfont=dict(color=COLORS["text2"]),
    ))
    layout = base_layout(340)
    layout["showlegend"] = False
    layout["yaxis"]["gridcolor"] = "rgba(0,0,0,0)"
    fig.update_layout(**layout)
    return fig


def build_gauge(score: int, color: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"size": 44, "color": COLORS["text"]}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": COLORS["text3"], "tickfont": {"color": COLORS["text3"]}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": COLORS["bg3"],
            "borderwidth": 0,
            "steps": [
                {"range": [0, 30], "color": "rgba(34,197,94,0.12)"},
                {"range": [30, 60], "color": "rgba(245,158,11,0.12)"},
                {"range": [60, 100], "color": "rgba(239,68,68,0.12)"},
            ],
        },
    ))
    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"]),
    )
    return fig


# =============================================================================
# UI SECTIONS
# =============================================================================
def render_hero() -> None:
    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:
        st.markdown(
            """
            <div class="hero-badge"><span class="badge-dot"></span> ML-Powered Prediction System</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 style='font-size:46px; line-height:1.1; margin-bottom:14px;'>"
            "Stop Churn Before It Starts</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='font-size:16px; color:{COLORS['text2']}; max-width:480px; line-height:1.7;'>"
            "An end-to-end machine learning platform that identifies at-risk customers "
            "with 94.2% accuracy — giving your team time to act before revenue walks out the door."
            "</p>",
            unsafe_allow_html=True,
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("Model Precision", "94.2%", "↑ accuracy")
        m2.metric("Revenue Retained", "$2.4M", "↑ saved")
        m3.metric("Profiles Analyzed", "18K", "customers")

    with col2:
        st.markdown('<div class="cg-card">', unsafe_allow_html=True)
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
            f"<span style='font-size:13px; font-weight:600; color:{COLORS['text2']}; text-transform:uppercase; letter-spacing:.06em;'>"
            "Customer Risk Score</span>"
            "<span class='risk-badge risk-high'>High Risk</span></div>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(build_gauge(78, COLORS["red"]), use_container_width=True, config={"displayModeBar": False})

        factors = [
            ("Contract Type", 85, COLORS["red"]),
            ("Monthly Charges", 72, COLORS["amber"]),
            ("Tenure", 60, COLORS["amber"]),
            ("Support Tickets", 45, COLORS["accent"]),
        ]
        for label, val, color in factors:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:10px; font-size:13px; margin-bottom:8px;">
                    <span style="width:110px; color:{COLORS['text2']};">{label}</span>
                    <div style="flex:1; height:6px; background:{COLORS['bg3']}; border-radius:999px; overflow:hidden;">
                        <div style="height:100%; width:{val}%; background:{color}; border-radius:999px;"></div>
                    </div>
                    <span style="width:36px; text-align:right; font-size:12px; color:{COLORS['text2']};">0.{val}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


def render_metrics() -> None:
    st.markdown('<p class="section-eyebrow">Performance Overview</p>', unsafe_allow_html=True)
    st.markdown("### Dashboard Metrics")
    st.markdown(
        '<p class="section-sub">Real-time monitoring of churn trends, model accuracy, '
        "and business impact across your customer base.</p>",
        unsafe_allow_html=True,
    )

    cards = [
        ("blue", "👥", COLORS["accent"], "18,420", "Total Customers", "trend-up", "↑ +3.2% this month"),
        ("green", "🛡️", COLORS["green"], "94.2%", "Prediction Accuracy", "trend-up", "↑ +1.8% vs last quarter"),
        ("amber", "⚠️", COLORS["amber"], "2,134", "At-Risk Customers", "trend-down", "↓ -12.4% from last month"),
        ("purple", "💰", COLORS["purple"], "$2.4M", "Revenue Saved", "trend-up", "↑ +28.6% YoY"),
    ]
    cols = st.columns(4)
    for col, (cls, icon, color, num, label, trend_cls, trend_text) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card {cls}">
                    <div class="metric-icon" style="background:{color}22; color:{color};">{icon}</div>
                    <div class="metric-num">{num}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-trend {trend_cls}">{trend_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    chart_col1, chart_col2 = st.columns([2, 1], gap="large")

    with chart_col1:
        st.markdown('<div class="cg-card">', unsafe_allow_html=True)
        st.markdown("**Churn Rate Over Time**")
        period = st.radio("Period", ["Monthly", "Quarterly"], horizontal=True, label_visibility="collapsed", key="trend_period")
        st.plotly_chart(build_churn_trend_chart(period), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="cg-card">', unsafe_allow_html=True)
        st.markdown("**Risk Distribution**")
        st.plotly_chart(build_risk_doughnut(), use_container_width=True, config={"displayModeBar": False})
        legend_rows = [
            ("Low Risk", "68% · 12,525", COLORS["green"]),
            ("Medium Risk", "20% · 3,684", COLORS["amber"]),
            ("High Risk", "12% · 2,210", COLORS["red"]),
        ]
        for label, val, color in legend_rows:
            st.markdown(
                f"""<div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;">
                <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{color};margin-right:6px;"></span>{label}</span>
                <strong>{val}</strong></div>""",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="cg-card">', unsafe_allow_html=True)
    st.markdown("**Feature Importance (SHAP Values)** — Top 8 predictive features")
    st.plotly_chart(build_feature_importance_chart(), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


def render_predictor() -> None:
    st.markdown('<p class="section-eyebrow">Live Demo</p>', unsafe_allow_html=True)
    st.markdown("### Predict Customer Churn")
    st.markdown(
        '<p class="section-sub">Enter customer attributes below to get an instant churn '
        "probability score with key risk factors and recommended actions.</p>",
        unsafe_allow_html=True,
    )

    form_col, result_col = st.columns([1, 1], gap="large")

    with form_col:
        st.markdown('<div class="cg-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Customer Profile")

        c1, c2 = st.columns(2)
        with c1:
            tenure = st.number_input("Tenure (months)", min_value=0, max_value=72, value=12)
            contract = st.selectbox("Contract Type", ["Month-to-Month", "One Year", "Two Year"])
            payment = st.selectbox("Payment Method", ["Electronic Check", "Mailed Check", "Auto Bank Transfer", "Credit Card"])
            tech_support = st.selectbox("Tech Support Subscription", ["No", "Yes"])
        with c2:
            charges = st.number_input("Monthly Charges ($)", min_value=0, value=85)
            internet = st.selectbox("Internet Service", ["Fiber Optic", "DSL", "No Internet"])
            tickets = st.number_input("Support Tickets", min_value=0, value=3)

        satisfaction = st.slider("Satisfaction Score", min_value=1, max_value=5, value=3)
        st.caption("1 = Very Unhappy · 5 = Very Happy")

        predict_clicked = st.button("🧠 Predict Churn Probability", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with result_col:
        st.markdown('<div class="cg-card">', unsafe_allow_html=True)

        if predict_clicked:
            with st.spinner("Analyzing customer profile..."):
                time.sleep(0.5)
                score = compute_churn_score(tenure, charges, contract, internet, payment, tickets, tech_support, satisfaction)
                factors = derive_risk_factors(tenure, charges, contract, tickets, tech_support, satisfaction)
                actions = derive_actions(tenure, charges, contract, tickets, satisfaction)
                band = risk_band(score)

                # Persist last result so it survives reruns triggered by other widgets
                st.session_state["last_prediction"] = {
                    "score": score, "factors": factors, "actions": actions, "band": band,
                    "confidence": round(91 + random.uniform(0, 6), 1),
                }

        result = st.session_state.get("last_prediction")

        if not result:
            st.markdown(
                f"""
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                            text-align:center; min-height:340px; color:{COLORS['text3']};">
                    <div style="font-size:46px; opacity:.3; margin-bottom:10px;">📊</div>
                    <div style="font-size:15px; font-weight:500; color:{COLORS['text2']};">Awaiting Input</div>
                    <div style="font-size:13px; max-width:280px;">Fill in the customer profile and click Predict
                    to see the churn probability score and risk factors.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            band = result["band"]
            st.markdown(
                f"<p style='font-size:13px; font-weight:700; color:{COLORS['text2']}; "
                "text-transform:uppercase; letter-spacing:.06em;'>Prediction Result</p>",
                unsafe_allow_html=True,
            )
            st.plotly_chart(build_gauge(result["score"], band["color"]), use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                f"<div style='text-align:center; margin-bottom:14px;'>"
                f"<span class='risk-badge {band['cls']}'>{band['label']}</span></div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<p style='font-size:13px; font-weight:700; color:{COLORS['text2']}; "
                "text-transform:uppercase; letter-spacing:.06em;'>Key Risk Factors</p>",
                unsafe_allow_html=True,
            )
            if not result["factors"]:
                st.caption("No significant risk factors detected")
            for f in result["factors"]:
                st.markdown(
                    f"""
                    <div class="factor-item">
                        <span>{f['label']}</span>
                        <div style="flex:1; height:6px; background:{COLORS['bg']}; border-radius:999px; margin:0 10px; overflow:hidden;">
                            <div style="height:100%; width:{int(f['impact']*100)}%; background:{f['color']}; border-radius:999px;"></div>
                        </div>
                        <span style="color:{f['color']}; font-weight:600;">{f['impact']:.2f}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"<p style='font-size:13px; font-weight:700; color:{COLORS['text2']}; "
                "text-transform:uppercase; letter-spacing:.06em; margin-top:10px;'>Recommended Actions</p>",
                unsafe_allow_html=True,
            )
            pills_html = "".join(f"<span class='action-pill {a['cls']}'>{a['text']}</span>" for a in result["actions"])
            st.markdown(pills_html, unsafe_allow_html=True)

            st.markdown(
                f"""
                <div style="margin-top:16px; padding:12px; background:{COLORS['bg3']}; border-radius:8px;
                            font-size:12px; color:{COLORS['text3']};">
                    ℹ️ Predictions generated by a heuristic scoring engine (demo). Confidence:
                    <span style="color:{COLORS['accent']};">{result['confidence']}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


def render_segments() -> None:
    st.markdown('<p class="section-eyebrow">Customer Segmentation</p>', unsafe_allow_html=True)
    st.markdown("### Risk Segments")
    st.markdown(
        '<p class="section-sub">Customers automatically grouped by churn likelihood using '
        "K-Means clustering and behavioral signals.</p>",
        unsafe_allow_html=True,
    )

    segments = [
        ("🛡️", COLORS["green"], "Loyal Champions", "12,525",
         "Long-tenure customers with strong engagement, auto-pay, and tech support. Churn risk under 15%.", 8),
        ("⚠️", COLORS["amber"], "At-Risk Fence Sitters", "3,684",
         "Month-to-month customers with rising charges and occasional complaints. Need proactive outreach.", 47),
        ("🔥", COLORS["red"], "Critical Churners", "2,211",
         "High charges, multiple tickets, no long-term contract. Immediate intervention required.", 83),
    ]
    cols = st.columns(3)
    for col, (icon, color, title, count, desc, pct) in zip(cols, segments):
        with col:
            st.markdown(
                f"""
                <div class="segment-card">
                    <div class="segment-icon" style="background:{color}22; color:{color};">{icon}</div>
                    <div style="font-size:15px; font-weight:600; margin-bottom:4px;">{title}</div>
                    <div style="font-size:26px; font-weight:700; color:{color}; margin-bottom:6px;">{count}</div>
                    <div style="font-size:13px; color:{COLORS['text2']}; line-height:1.5; margin-bottom:14px;">{desc}</div>
                    <div style="display:flex; justify-content:space-between; font-size:12px; color:{COLORS['text3']}; margin-bottom:6px;">
                        <span>Avg Churn Risk</span><span style="color:{color};">{pct}.0%</span>
                    </div>
                    <div style="height:6px; background:{COLORS['bg3']}; border-radius:999px; overflow:hidden;">
                        <div style="height:100%; width:{pct}%; background:{color}; border-radius:999px;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_insights() -> None:
    st.markdown('<p class="section-eyebrow">Model Insights</p>', unsafe_allow_html=True)
    st.markdown("### What Drives Churn?")
    st.markdown(
        '<p class="section-sub">SHAP analysis and exploratory data analysis reveal the most '
        "impactful signals in customer behavior.</p>",
        unsafe_allow_html=True,
    )

    insights = [
        ("📄", COLORS["red"], "Contract Type is the #1 Predictor",
         "Month-to-month customers are 3.4× more likely to churn than customers on annual or "
         "bi-annual contracts. Nudging at-risk customers toward longer contracts reduces churn significantly.",
         "3.4×", "higher churn rate for month-to-month vs annual"),
        ("💵", COLORS["amber"], "High Charges Without Perceived Value",
         "Customers paying over $80/month who don't use Tech Support or Online Backup are 2.1× more "
         "likely to leave. Perceived value gap triggers churn faster than price alone.",
         "2.1×", "higher risk when charges exceed value perception"),
        ("⏱️", COLORS["accent"], "The Critical First 12 Months",
         "60% of churners leave within their first year. The onboarding experience and early value "
         "delivery are the most important retention levers available to the business.",
         "60%", "of churners leave within year one"),
        ("🎧", COLORS["purple"], "Support Tickets as an Early Warning",
         "Customers who raise 3+ support tickets in 6 months have a 58% churn probability. Each "
         "unresolved ticket increases churn risk by an estimated 8 percentage points.",
         "+8pp", "churn risk per unresolved support ticket"),
    ]
    cols = st.columns(2)
    for i, (icon, color, title, desc, stat_num, stat_label) in enumerate(insights):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="insight-card">
                    <div style="display:flex; gap:12px; margin-bottom:12px;">
                        <div style="width:36px; height:36px; border-radius:10px; background:{color}22; color:{color};
                                    display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0;">{icon}</div>
                        <div>
                            <div style="font-size:14px; font-weight:600; margin-bottom:4px;">{title}</div>
                            <div style="font-size:13px; color:{COLORS['text2']}; line-height:1.5;">{desc}</div>
                        </div>
                    </div>
                    <div style="display:flex; align-items:baseline; gap:6px; padding-top:12px; border-top:1px solid {COLORS['border']};">
                        <span style="font-size:22px; font-weight:700; color:{color};">{stat_num}</span>
                        <span style="font-size:13px; color:{COLORS['text2']};">{stat_label}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")


def render_pipeline() -> None:
    st.markdown('<p class="section-eyebrow">Technical Architecture</p>', unsafe_allow_html=True)
    st.markdown("### ML Pipeline")
    st.markdown(
        '<p class="section-sub">A production-grade machine learning pipeline from raw data '
        "ingestion to real-time churn scoring.</p>",
        unsafe_allow_html=True,
    )

    step_titles = [f"{s['icon']} {s['title']}" for s in PIPELINE_STEPS]
    selected_label = st.radio(
        "Pipeline stage", step_titles, index=2, horizontal=True,
        label_visibility="collapsed", key="pipeline_stage",
    )
    selected_idx = step_titles.index(selected_label)
    step = PIPELINE_STEPS[selected_idx]

    st.markdown('<div class="cg-card">', unsafe_allow_html=True)
    st.markdown(f"#### {step['title']}")
    st.caption(step["sub"])
    st.code(step["code"], language="python")

    if selected_idx == 2:
        m1, m2, m3 = st.columns(3)
        m1.metric("AUC-ROC", "94.2%")
        m2.metric("Precision", "91.6%")
        m3.metric("Recall", "88.3%")
    st.markdown("</div>", unsafe_allow_html=True)


def render_customers_table() -> None:
    st.markdown('<p class="section-eyebrow">Customer Intelligence</p>', unsafe_allow_html=True)
    st.markdown("### Customer Risk Table")
    st.markdown(
        '<p class="section-sub">Browse and search all customer profiles with live churn '
        "scores and recommended interventions.</p>",
        unsafe_allow_html=True,
    )

    df = load_customers()

    search_col, filter_col = st.columns([2, 1])
    with search_col:
        query = st.text_input("Search customers", placeholder="Search by name or ID…", label_visibility="collapsed")
    with filter_col:
        level_filter = st.selectbox("Risk level", ["All", "High", "Medium", "Low"], label_visibility="collapsed")

    filtered = df.copy()
    if level_filter != "All":
        filtered = filtered[filtered["Risk Level"] == level_filter]
    if query:
        q = query.lower()
        filtered = filtered[
            filtered["Customer"].str.lower().str.contains(q) | filtered["ID"].str.lower().str.contains(q)
        ]

    def style_risk(val):
        color = COLORS["red"] if val == "High" else COLORS["amber"] if val == "Medium" else COLORS["green"]
        return f"color: {color}; font-weight: 600;"

    styler = filtered.style
    # pandas >= 2.1 renamed Styler.applymap to Styler.map; support both
    # so the app works across the range of pandas versions Streamlit Cloud
    # may resolve at install time.
    if hasattr(styler, "map"):
        styler = styler.map(style_risk, subset=["Risk Level"])
    else:  # pragma: no cover - legacy pandas fallback
        styler = styler.applymap(style_risk, subset=["Risk Level"])

    st.dataframe(
        styler,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Churn Risk %": st.column_config.ProgressColumn(
                "Churn Risk %", min_value=0, max_value=100, format="%d%%"
            ),
        },
    )
    st.caption(f"Showing {len(filtered)} of {len(df)} customers")


def render_tech_stack() -> None:
    st.markdown('<p class="section-eyebrow">Built With</p>', unsafe_allow_html=True)
    st.markdown("### Technology Stack")

    stack = [
        ("🐍", "Python 3.11", "Core ML pipeline language"),
        ("⚡", "XGBoost + RF", "Ensemble gradient boosting"),
        ("🔍", "SHAP", "Model explainability layer"),
        ("🚀", "FastAPI", "Real-time prediction API"),
        ("🐳", "Docker", "Containerized deployment"),
        ("📊", "Pandas / NumPy", "Feature engineering"),
        ("🧪", "Scikit-learn", "Preprocessing & evaluation"),
        ("☁️", "Streamlit Cloud", "App hosting & deployment"),
    ]
    cols = st.columns(4)
    for i, (icon, name, desc) in enumerate(stack):
        with cols[i % 4]:
            st.markdown(
                f"""
                <div class="cg-card" style="text-align:center; margin-bottom:14px;">
                    <div style="font-size:28px; margin-bottom:8px;">{icon}</div>
                    <div style="font-size:14px; font-weight:600;">{name}</div>
                    <div style="font-size:12px; color:{COLORS['text2']};">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## 📡 ChurnGuard")
        st.caption("Customer Churn Prediction Platform")
        st.markdown("---")
        page = st.radio(
            "Navigate",
            ["Overview", "Predict", "Analytics", "Segments", "Pipeline", "Customers"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.caption("Built as a portfolio project demonstrating an end-to-end ML churn prediction workflow.")
        st.caption("⚠️ Predictions use a transparent heuristic engine for demo purposes — not a trained model.")
    return page


# =============================================================================
# MAIN APP
# =============================================================================
def main() -> None:
    inject_css()
    page = render_sidebar()

    if page == "Overview":
        render_hero()
        st.markdown("---")
        render_tech_stack()
    elif page == "Predict":
        render_predictor()
    elif page == "Analytics":
        render_metrics()
        st.markdown("---")
        render_insights()
    elif page == "Segments":
        render_segments()
    elif page == "Pipeline":
        render_pipeline()
    elif page == "Customers":
        render_customers_table()


if __name__ == "__main__":
    main()
