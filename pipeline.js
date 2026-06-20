/* =========================================================================
   pipeline.js
   Powers the interactive "ML Pipeline" step-through component:
   clicking a step updates the detail panel's title, description,
   syntax-highlighted code snippet, and the visual step progress trail.
   ========================================================================= */

/**
 * Content for each of the 5 pipeline stages.
 * `code` is pre-formatted HTML with manual syntax-highlight spans
 * (kw = keyword, fn = function/class, str = string, cm = comment, num = number)
 * matching the .code-block span classes defined in style.css.
 */
const PIPELINE_CONTENT = [
  {
    title: 'Data Ingestion & ETL',
    sub: 'Pulling from CRM, billing systems, and customer support platforms',
    code:
`<span class="kw">import</span> pandas <span class="kw">as</span> pd
<span class="kw">from</span> sqlalchemy <span class="kw">import</span> create_engine

<span class="cm"># Connect to data sources</span>
engine = create_engine(<span class="str">'postgresql://...'</span>)
crm_df = pd.<span class="fn">read_sql</span>(<span class="str">'SELECT * FROM customers'</span>, engine)
billing_df = pd.<span class="fn">read_sql</span>(<span class="str">'SELECT * FROM billing'</span>, engine)

<span class="cm"># Merge datasets</span>
df = crm_df.<span class="fn">merge</span>(billing_df, on=<span class="str">'customer_id'</span>)
<span class="fn">print</span>(<span class="str">f"Loaded {len(df):,} records"</span>)
<span class="cm"># Output: Loaded 50,000 records</span>`
  },
  {
    title: 'Feature Engineering',
    sub: 'Creating 38 behavioral and transactional features from raw signals',
    code:
`<span class="kw">def</span> <span class="fn">engineer_features</span>(df):
    <span class="cm"># Tenure buckets</span>
    df[<span class="str">'tenure_bin'</span>] = pd.<span class="fn">cut</span>(df[<span class="str">'tenure'</span>], bins=[<span class="num">0</span>,<span class="num">12</span>,<span class="num">24</span>,<span class="num">48</span>,<span class="num">72</span>])

    <span class="cm"># Charge to tenure ratio</span>
    df[<span class="str">'charge_per_month'</span>] = df[<span class="str">'total_charges'</span>] / (df[<span class="str">'tenure'</span>]+<span class="num">1</span>)

    <span class="cm"># Interaction features</span>
    df[<span class="str">'no_support_high_charge'</span>] = (
        (df[<span class="str">'monthly_charges'</span>] > <span class="num">80</span>) &
        (df[<span class="str">'tech_support'</span>] == <span class="str">'No'</span>)
    ).<span class="fn">astype</span>(int)
    <span class="kw">return</span> df`
  },
  {
    title: 'Model Training — XGBoost Ensemble',
    sub: 'Gradient boosted trees with cross-validation and hyperparameter tuning via Optuna',
    code:
`<span class="kw">import</span> xgboost <span class="kw">as</span> xgb
<span class="kw">from</span> sklearn.model_selection <span class="kw">import</span> StratifiedKFold

<span class="cm"># Define ensemble model</span>
xgb_model = xgb.<span class="fn">XGBClassifier</span>(
    n_estimators=<span class="num">500</span>,
    learning_rate=<span class="num">0.05</span>,
    max_depth=<span class="num">6</span>,
    subsample=<span class="num">0.8</span>,
    eval_metric=<span class="str">'auc'</span>
)

<span class="cm"># 5-fold cross-validation</span>
cv = <span class="fn">StratifiedKFold</span>(n_splits=<span class="num">5</span>, shuffle=<span class="kw">True</span>)
scores = cross_val_score(xgb_model, X_train, y_train, cv=cv)
<span class="fn">print</span>(<span class="str">f"Mean AUC: {scores.mean():.4f}"</span>)
<span class="cm"># Output: Mean AUC: 0.9421</span>`
  },
  {
    title: 'Model Evaluation & SHAP',
    sub: 'Measuring performance and explaining predictions with SHAP values',
    code:
`<span class="kw">import</span> shap

<span class="cm"># SHAP explainer</span>
explainer = shap.<span class="fn">TreeExplainer</span>(xgb_model)
shap_values = explainer.<span class="fn">shap_values</span>(X_test)

<span class="cm"># Evaluate model</span>
from sklearn.metrics <span class="kw">import</span> roc_auc_score, classification_report
y_pred = xgb_model.<span class="fn">predict_proba</span>(X_test)[:,<span class="num">1</span>]
auc = <span class="fn">roc_auc_score</span>(y_test, y_pred)
<span class="fn">print</span>(<span class="str">f"Test AUC: {auc:.4f}"</span>)
<span class="cm"># Output: Test AUC: 0.9418</span>`
  },
  {
    title: 'API Deployment with FastAPI',
    sub: 'Serving predictions as a REST API with Docker containerization',
    code:
`<span class="kw">from</span> fastapi <span class="kw">import</span> FastAPI
<span class="kw">from</span> pydantic <span class="kw">import</span> BaseModel

app = <span class="fn">FastAPI</span>(title=<span class="str">"ChurnGuard API"</span>)

<span class="kw">class</span> <span class="fn">CustomerData</span>(BaseModel):
    tenure: int
    monthly_charges: float
    contract: str
    tech_support: str

@app.<span class="fn">post</span>(<span class="str">"/predict"</span>)
<span class="kw">async def</span> <span class="fn">predict_churn</span>(data: CustomerData):
    features = preprocess(data)<span class="cm">  # transform input</span>
    prob = model.<span class="fn">predict_proba</span>(features)[<span class="num">0</span>,<span class="num">1</span>]
    <span class="kw">return</span> {<span class="str">"churn_probability"</span>: <span class="fn">round</span>(float(prob),<span class="num">4</span>)}`
  }
];

/**
 * Updates the active/done state of each step button in the trail,
 * then populates the detail panel for the selected step index.
 * @param {number} index - 0-4
 */
function showPipelineStep(index) {
  const steps = document.querySelectorAll('.pipeline-step');

  steps.forEach((step, i) => {
    step.classList.remove('active');
    if (i < index) {
      step.classList.add('done');
    } else {
      step.classList.remove('done');
    }
  });

  steps[index].classList.add('active');

  const data = PIPELINE_CONTENT[index];
  document.getElementById('pd_title').textContent = data.sub ? data.title : data.title;
  document.getElementById('pd_sub').textContent = data.sub;

  const codeEl = document.querySelector('#pd_code code');
  codeEl.innerHTML = data.code;
}
