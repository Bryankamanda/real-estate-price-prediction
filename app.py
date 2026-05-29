import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Japan Car Import Advisory | Kenya",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* Root theme */
    :root {
        --accent: #E8FF00;
        --accent-dim: #c8dd00;
        --dark: #0D0D0D;
        --mid: #1A1A1A;
        --surface: #222222;
        --border: #333333;
        --text-primary: #F5F5F5;
        --text-secondary: #999999;
        --success: #00E676;
        --warning: #FF6D00;
    }

    /* Global overrides */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background-color: var(--dark);
        color: var(--text-primary);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--mid) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] .stSlider label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.78rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-secondary) !important;
    }

    /* Hero header */
    .hero-wrap {
        background: linear-gradient(135deg, #0D0D0D 0%, #1a1a1a 50%, #0D0D0D 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-wrap::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 280px; height: 280px;
        background: radial-gradient(circle, rgba(232,255,0,0.08) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(232,255,0,0.12);
        border: 1px solid rgba(232,255,0,0.3);
        color: var(--accent);
        font-family: 'DM Sans', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 4px 14px;
        border-radius: 100px;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.1;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
    }
    .hero-title span {
        color: var(--accent);
    }
    .hero-sub {
        font-size: 1rem;
        color: var(--text-secondary);
        font-weight: 300;
        margin: 0;
    }

    /* Metric cards */
    .metric-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        transition: border-color 0.2s;
    }
    .metric-card:hover { border-color: #555; }
    .metric-card.accent-card {
        background: rgba(232,255,0,0.06);
        border-color: rgba(232,255,0,0.35);
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    .metric-value.yellow { color: var(--accent); }
    .metric-value.green  { color: var(--success); }
    .metric-value.orange { color: var(--warning); }
    .metric-sub {
        font-size: 0.78rem;
        color: var(--text-secondary);
        margin-top: 0.35rem;
    }

    /* Section headers */
    .section-header {
        font-family: 'Syne', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--accent);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
    }

    /* Breakdown table */
    .breakdown-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }
    .breakdown-table th {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-secondary);
        padding: 0.6rem 1rem;
        text-align: left;
        border-bottom: 1px solid var(--border);
    }
    .breakdown-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: var(--text-primary);
    }
    .breakdown-table tr:last-child td {
        border-bottom: none;
        font-weight: 700;
        font-family: 'Syne', sans-serif;
        color: var(--accent);
    }
    .breakdown-table .amount {
        text-align: right;
        font-variant-numeric: tabular-nums;
    }

    /* Alert banners */
    .alert-success {
        background: rgba(0, 230, 118, 0.08);
        border: 1px solid rgba(0, 230, 118, 0.35);
        border-left: 4px solid var(--success);
        border-radius: 10px;
        padding: 1rem 1.4rem;
        color: var(--success);
        font-weight: 500;
        margin-top: 1.5rem;
    }
    .alert-warning {
        background: rgba(255, 109, 0, 0.08);
        border: 1px solid rgba(255, 109, 0, 0.35);
        border-left: 4px solid var(--warning);
        border-radius: 10px;
        padding: 1rem 1.4rem;
        color: var(--warning);
        font-weight: 500;
        margin-top: 1.5rem;
    }
    .alert-icon { font-size: 1.2rem; margin-right: 0.5rem; }

    /* Sidebar section divider */
    .sidebar-section {
        font-family: 'Syne', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: var(--accent) !important;
        margin: 1.2rem 0 0.4rem 0;
    }

    /* Hide Streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)


# ── Load Model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("car_price_predictor.pkl")

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)


# ── Sidebar Inputs ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-section">🚗 Vehicle Specs</p>', unsafe_allow_html=True)

    make = st.selectbox(
        "Make",
        options=["TOYOTA", "HONDA", "NISSAN", "SUZUKI", "MAZDA", "SUBARU", "BMW"],
        index=0,
    )
    car_model = st.text_input("Model", value="COROLLA")
    mileage = st.number_input("Mileage (km)", min_value=0, max_value=300000,
                               value=60000, step=5000)
    engine_cc = st.number_input("Engine Capacity (cc)", min_value=600, max_value=5000,
                                 value=1500, step=100)

    st.markdown('<p class="sidebar-section">⚙️ Configuration</p>', unsafe_allow_html=True)

    transmission = st.selectbox(
        "Transmission",
        options=["AT", "MT", "CVT", "5MT"],
        index=0,
    )
    fuel_type = st.selectbox(
        "Fuel Type",
        options=["PETROL", "DIESEL", "HYBRID(PETROL)", "ELECTRIC"],
        index=0,
    )
    drive_type = st.selectbox(
        "Drive Type",
        options=["2WD", "4WD"],
        index=0,
    )

    st.markdown('<p class="sidebar-section">📅 Age</p>', unsafe_allow_html=True)

    car_age = st.slider("Car Age (years)", min_value=0, max_value=20, value=5)

    st.markdown("---")
    predict_btn = st.button("🔍 Analyse Import", use_container_width=True, type="primary")


# ── Hero Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🇯🇵 Japan → 🇰🇪 Kenya</div>
    <h1 class="hero-title">Japan Car<br><span>Import Advisory</span></h1>
    <p class="hero-sub">AI-powered pricing intelligence for smart vehicle imports into Kenya</p>
</div>
""", unsafe_allow_html=True)


# ── Model status warning ───────────────────────────────────────────────────────
if not model_loaded:
    st.error(f"⚠️ Could not load model: `{model_error}`. Make sure `car_price_predictor.pkl` is in the same directory as `app.py`.")
    st.stop()


# ── Core Logic ─────────────────────────────────────────────────────────────────
def compute_import_costs(predicted_price_jpy: float, engine_cc: int) -> dict:
    """Compute full Kenya import cost breakdown from Japan auction price (JPY)."""
    exchange_rate    = 1.05
    shipping_cost    = 120_000
    clearing_fees    = 50_000
    registration_cost= 10_000

    # CIF in KES
    cif = predicted_price_jpy * exchange_rate + shipping_cost

    # Duties & taxes
    import_duty  = 0.25 * cif
    excise_rate  = 0.20 if engine_cc <= 1500 else 0.25
    excise_duty  = excise_rate * cif
    vat          = 0.16 * (cif + import_duty + excise_duty)
    rdl          = 0.02 * cif

    total_taxes = import_duty + excise_duty + vat + rdl

    final_import_cost = cif + total_taxes + clearing_fees + registration_cost
    local_market_price = final_import_cost + 300_000
    savings = local_market_price - final_import_cost

    return {
        "predicted_price_jpy": predicted_price_jpy,
        "cif":                 cif,
        "import_duty":         import_duty,
        "excise_duty":         excise_duty,
        "excise_rate":         excise_rate,
        "vat":                 vat,
        "rdl":                 rdl,
        "clearing_fees":       clearing_fees,
        "registration_cost":   registration_cost,
        "total_taxes":         total_taxes,
        "final_import_cost":   final_import_cost,
        "local_market_price":  local_market_price,
        "savings":             savings,
    }


def fmt(val: float, prefix: str = "KES") -> str:
    return f"{prefix} {val:,.0f}"

def fmt_jpy(val: float) -> str:
    return f"¥ {val:,.0f}"


# ── Build input dataframe ──────────────────────────────────────────────────────
input_df = pd.DataFrame({
    "make":         [make],
    "model":        [car_model],
    "mileage":      [mileage],
    "engine_cc":    [engine_cc],
    "transmission": [transmission],
    "fuel_type":    [fuel_type],
    "drive_type":   [drive_type],
    "car_age":      [car_age],
})


# ── Run prediction & display results ──────────────────────────────────────────
if predict_btn or True:          # always show results; recalculates on any widget change
    try:
        predicted_price = float(model.predict(input_df)[0])
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.stop()

    costs = compute_import_costs(predicted_price, engine_cc)

    # ── Top KPI cards ──────────────────────────────────────────────────────────
    st.markdown('<p class="section-header">📊 Cost Summary</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Japan Auction Price</div>
            <div class="metric-value yellow">{fmt_jpy(costs['predicted_price_jpy'])}</div>
            <div class="metric-sub">Estimated JPY at auction</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CIF Value</div>
            <div class="metric-value">{fmt(costs['cif'])}</div>
            <div class="metric-sub">Cost + Insurance + Freight</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card accent-card">
            <div class="metric-label">Total Import Cost</div>
            <div class="metric-value yellow">{fmt(costs['final_import_cost'])}</div>
            <div class="metric-sub">All-in landed cost (Kenya)</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        savings_color = "green" if costs["savings"] > 0 else "orange"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Potential Savings</div>
            <div class="metric-value {savings_color}">{fmt(costs['savings'])}</div>
            <div class="metric-sub">vs estimated local market</div>
        </div>""", unsafe_allow_html=True)

    # ── Two-column layout: breakdown + comparison ──────────────────────────────
    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown('<p class="section-header">🧾 Import Cost Breakdown</p>', unsafe_allow_html=True)
        breakdown_rows = [
            ("CIF Value",              costs["cif"]),
            (f"Import Duty (25%)",      costs["import_duty"]),
            (f"Excise Duty ({int(costs['excise_rate']*100)}%)",
                                        costs["excise_duty"]),
            ("VAT (16%)",              costs["vat"]),
            ("RDL (2%)",               costs["rdl"]),
            ("Clearing Fees",          costs["clearing_fees"]),
            ("Registration Cost",      costs["registration_cost"]),
            ("TOTAL IMPORT COST",      costs["final_import_cost"]),
        ]

        rows_html = ""
        for label, amount in breakdown_rows:
            rows_html += f"""
            <tr>
                <td>{label}</td>
                <td class="amount">{fmt(amount)}</td>
            </tr>"""

        st.markdown(f"""
        <table class="breakdown-table">
            <thead>
                <tr>
                    <th>Component</th>
                    <th class="amount">Amount (KES)</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>""", unsafe_allow_html=True)

    with right:
        st.markdown('<p class="section-header">🏷️ Price Comparison</p>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card" style="margin-bottom:1rem">
            <div class="metric-label">Import Cost (All-in)</div>
            <div class="metric-value yellow">{fmt(costs['final_import_cost'])}</div>
            <div class="metric-sub">Japan auction → Kenyan road</div>
        </div>
        <div class="metric-card" style="margin-bottom:1rem">
            <div class="metric-label">Est. Local Market Price</div>
            <div class="metric-value">{fmt(costs['local_market_price'])}</div>
            <div class="metric-sub">Typical dealer markup + KES 300K</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">You Save</div>
            <div class="metric-value {'green' if costs['savings']>0 else 'orange'}">{fmt(costs['savings'])}</div>
            <div class="metric-sub">By importing directly</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Recommendation banner ──────────────────────────────────────────────
        if costs["savings"] > 0:
            st.markdown(f"""
            <div class="alert-success">
                <span class="alert-icon">✅</span>
                <strong>Good Import Deal!</strong><br>
                Importing this <strong>{make} {car_model}</strong> may save you
                <strong>{fmt(costs['savings'])}</strong> compared to buying locally.
                Proceed with confidence.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-warning">
                <span class="alert-icon">⚠️</span>
                <strong>Consider Local Market</strong><br>
                For this <strong>{make} {car_model}</strong>, buying locally may be cheaper
                given current duty rates and shipping costs.
            </div>""", unsafe_allow_html=True)

    # ── Vehicle summary strip ──────────────────────────────────────────────────
    st.markdown('<p class="section-header">🔧 Vehicle Specification</p>', unsafe_allow_html=True)

    spec_cols = st.columns(8)
    specs = [
        ("Make",         make),
        ("Model",        car_model),
        ("Mileage",      f"{mileage:,} km"),
        ("Engine",       f"{engine_cc} cc"),
        ("Transmission", transmission),
        ("Fuel",         fuel_type),
        ("Drive",        drive_type),
        ("Age",          f"{car_age} yr{'s' if car_age != 1 else ''}"),
    ]
    for col, (label, val) in zip(spec_cols, specs):
        with col:
            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid var(--border);
                        border-radius:8px;padding:0.7rem 0.8rem;text-align:center;">
                <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.09em;
                            color:var(--text-secondary);margin-bottom:0.3rem;">{label}</div>
                <div style="font-family:'Syne',sans-serif;font-size:0.85rem;
                            font-weight:700;color:var(--text-primary);">{val}</div>
            </div>""", unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:3rem;padding-top:1.5rem;border-top:1px solid #222;
                text-align:center;color:#444;font-size:0.75rem;">
        Japan Car Import Advisory Platform · Estimates based on Kenya Revenue Authority duty schedules ·
        Exchange rate & shipping costs indicative only · Always verify with a licensed clearing agent
    </div>""", unsafe_allow_html=True)




