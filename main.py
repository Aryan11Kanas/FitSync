import streamlit as st
import pandas as pd
from modules.processor import process_data
from modules.theme import init_theme, render_theme_toggle, apply_custom_css, get_current_theme

# Page Configuration
st.set_page_config(
    page_title="FitSync — Personal Health Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme and inject custom CSS
init_theme()
apply_custom_css()
render_theme_toggle()

# Cached data loader
@st.cache_data
def get_cached_data():
    return process_data()

try:
    df = get_cached_data().copy()
    data_loaded = True
except Exception as e:
    df = pd.DataFrame()
    data_loaded = False
    load_error = str(e)

theme = get_current_theme()
is_dark = st.session_state.get("theme", "dark") == "dark"

# --- HERO SECTION ---
st.markdown(f"""
<div class="hero-container">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
        <span class="hero-badge">
            <span class="live-dot"></span> BIOMETRIC INTELLIGENCE ENGINE
        </span>
        <span style="font-size: 0.8rem; font-weight: 600; color: {theme['text_muted']}; letter-spacing: 0.5px;">
            SYSTEM STATUS: <span style="color: {theme['primary']}; font-weight: 700;">ONLINE</span>
        </span>
    </div>
    <h1 class="hero-title">FitSync — Personal Health Intelligence</h1>
    <p class="hero-subtitle">
        Empowering individuals to unlock physiological patterns from wearable fitness tracking.
        FitSync cleanses raw telemetry, computes a multi-factor <strong>Recovery Score</strong>,
        and provides interactive visual intelligence across sleep, physical activity, and cardiovascular strain.
    </p>
</div>
""", unsafe_allow_html=True)

# --- QUICK STATS SUMMARY BAR ---
if data_loaded and not df.empty:
    total_days = len(df)
    avg_steps = df['Steps'].mean()
    avg_sleep = df['Sleep_Hours'].mean()
    avg_recovery = df['Recovery_Score'].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">
                <span>Monitored Window</span>
                <span>📅</span>
            </div>
            <div class="kpi-value">{total_days} <span style="font-size: 1.1rem; font-weight: 600; color:{theme['text_muted']};">Days</span></div>
            <div class="kpi-subtitle">Continuous biometric telemetry</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        step_color = theme['primary'] if avg_steps >= 10000 else theme['accent_amber']
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">
                <span>Daily Steps Average</span>
                <span>👟</span>
            </div>
            <div class="kpi-value" style="color: {step_color} !important;">{avg_steps:,.0f}</div>
            <div class="kpi-subtitle">
                <span style="padding: 2px 6px; border-radius: 4px; background: {theme['primary_glow']}; color: {theme['primary']}; font-weight: 700; font-size: 0.72rem;">Goal: 10,000</span>
                <span>daily average</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        sleep_color = theme['primary'] if avg_sleep >= 7.0 else theme['accent_amber']
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">
                <span>Sleep Duration Average</span>
                <span>🌙</span>
            </div>
            <div class="kpi-value" style="color: {sleep_color} !important;">{avg_sleep:.1f} <span style="font-size: 1.1rem; font-weight: 600; color:{theme['text_muted']};">hrs</span></div>
            <div class="kpi-subtitle">
                <span style="padding: 2px 6px; border-radius: 4px; background: {theme['primary_glow']}; color: {theme['primary']}; font-weight: 700; font-size: 0.72rem;">Target: 7-9h</span>
                <span>rest benchmark</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        recovery_color = theme['primary'] if avg_recovery >= 70 else theme['accent_amber'] if avg_recovery >= 50 else theme['accent_rose']
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">
                <span>Mean Recovery Score</span>
                <span>⚡</span>
            </div>
            <div class="kpi-value" style="color: {recovery_color} !important;">{avg_recovery:.1f}<span style="font-size: 1.1rem; font-weight: 500; color:{theme['text_muted']};">/100</span></div>
            <div class="kpi-subtitle">
                <span style="padding: 2px 6px; border-radius: 4px; background: {theme['primary_glow']}; color: {theme['primary']}; font-weight: 700; font-size: 0.72rem;">WHOOP Scale</span>
                <span>composite readiness</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- CORE FEATURES GRID ---
st.markdown("### 🚀 Core Platform Capabilities")
feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-icon">📊</div>
        <h3 class="card-title">Dynamic KPI Dashboard</h3>
        <p class="card-body">
            Examine key performance indicators including step cadence, sleep duration, resting heart rate, and readiness score across 7-day, 30-day, 90-day, and all-time interactive windows.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-icon">🧠</div>
        <h3 class="card-title">Algorithmic Recovery</h3>
        <p class="card-body">
            Computes physiological readiness using a multi-factor algorithm combining sleep sufficiency, resting cardiac rate, and step distribution clamped between 0 and 100.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-icon">📈</div>
        <h3 class="card-title">Statistical Trends & EDA</h3>
        <p class="card-body">
            Explore metric distributions, day-of-week rhythms, monthly recovery aggregations, and Pearson correlation matrices rendered with responsive Plotly visualizations.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- HOW IT WORKS (3-STEP PIPELINE) ---
st.markdown("### ⚙️ How FitSync Works")
step_col1, step_col2, step_col3 = st.columns(3)

with step_col1:
    st.markdown(f"""
    <div class="custom-card">
        <div style="display:flex; align-items:center; margin-bottom: 12px;">
            <span class="step-badge">01</span>
            <strong style="font-size: 1.1rem; color: {theme['text']};">Data Imputation</strong>
        </div>
        <p class="card-body">
            Ingests daily biometric CSV records and imputes missing sensor telemetry using statistical medians and clinical baseline anchors.
        </p>
    </div>
    """, unsafe_allow_html=True)

with step_col2:
    st.markdown(f"""
    <div class="custom-card">
        <div style="display:flex; align-items:center; margin-bottom: 12px;">
            <span class="step-badge">02</span>
            <strong style="font-size: 1.1rem; color: {theme['text']};">Score Computation</strong>
        </div>
        <p class="card-body">
            Applies tiered scoring weights to evaluate sleep quantity, resting heart rate, and optimal step ranges clamped strictly to 0-100.
        </p>
    </div>
    """, unsafe_allow_html=True)

with step_col3:
    st.markdown(f"""
    <div class="custom-card">
        <div style="display:flex; align-items:center; margin-bottom: 12px;">
            <span class="step-badge">03</span>
            <strong style="font-size: 1.1rem; color: {theme['text']};">Interactive Exploration</strong>
        </div>
        <p class="card-body">
            Presents findings through high-performance cached Streamlit pages with customizable filters, responsive charts, and instant theme toggling.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- DATA PREVIEW SECTION ---
st.markdown("### 📋 Cleaned Telemetry Preview")
if data_loaded and not df.empty:
    with st.expander("🔍 Click to inspect processed dataset records (First 10 records)", expanded=True):
        st.dataframe(
            df.head(10).style.format({
                "Steps": "{:.0f}",
                "Sleep_Hours": "{:.1f}",
                "Heart_Rate_bpm": "{:.1f}",
                "Calories_Burned": "{:.0f}",
                "Active_Minutes": "{:.0f}",
                "Recovery_Score": "{:.0f}"
            }),
            use_container_width=True
        )
        st.caption(f"Displaying 10 of {len(df)} cleaned and scored biometric records.")
else:
    st.error(f"Unable to load data/health_data.csv: {load_error if 'load_error' in locals() else 'File not found'}. Run `python generate_data.py` to create the dataset.")

# --- CALL TO ACTION & FOOTER ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="
    background: {theme['card_bg']};
    border: 1px solid {theme['card_border']};
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(12px);
    box-shadow: {theme['shadow']};
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
">
    <div>
        <div style="font-size: 1.15rem; font-weight: 700; color: {theme['text']}; margin-bottom: 4px;">
            ⚡ Ready to analyze your health telemetry?
        </div>
        <div style="font-size: 0.9rem; color: {theme['text_muted']};">
            Navigate to <strong>1_Dashboard</strong> or <strong>2_Trends</strong> via the sidebar to start exploring.
        </div>
    </div>
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 10px;
        background: {theme['primary_glow']};
        border: 1px solid {theme['primary']};
        color: {theme['primary']};
        font-weight: 700;
        font-size: 0.85rem;
    ">
        Use Sidebar Navigation 👈
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="fitsync-footer">
    <strong>FitSync</strong> &bull; Personal Health Analytics Platform &bull; Designed & Developed by <strong>FitSync Team</strong>
</div>
""", unsafe_allow_html=True)
