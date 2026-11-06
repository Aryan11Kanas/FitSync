import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from modules.processor import process_data
from modules.theme import init_theme, render_theme_toggle, apply_custom_css, style_plotly_chart, get_current_theme

# Page Configuration
st.set_page_config(
    page_title="FitSync — Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme and custom CSS
init_theme()
apply_custom_css()
render_theme_toggle()
theme = get_current_theme()
is_dark = st.session_state.get("theme", "dark") == "dark"

# --- CACHED DATA PIPELINE ---
@st.cache_data
def get_cached_health_data():
    """
    Loads and caches processed health data to optimize UI responsiveness.
    """
    return process_data()

# Ensure we operate on a copy to prevent mutating cached state
full_df = get_cached_health_data().copy()

# --- SIDEBAR FILTERS ---
st.sidebar.markdown(f"""
<div style="
    background: {theme['card_bg']};
    border: 1px solid {theme['card_border']};
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 14px;
">
    <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: {theme['text_muted']};">
        🔍 Telemetry Filters
    </div>
</div>
""", unsafe_allow_html=True)

time_range = st.sidebar.selectbox(
    "Select Time Window",
    options=["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
    index=1
)

# Filter dataset
df = full_df.copy()
if 'Date' in df.columns and not df.empty:
    max_date = df['Date'].max()
    if time_range == "Last 7 Days":
        df = df[df['Date'] >= (max_date - pd.Timedelta(days=7))].copy()
    elif time_range == "Last 30 Days":
        df = df[df['Date'] >= (max_date - pd.Timedelta(days=30))].copy()
    elif time_range == "Last 90 Days":
        df = df[df['Date'] >= (max_date - pd.Timedelta(days=90))].copy()
    
    df = df.sort_values('Date').reset_index(drop=True)

st.sidebar.markdown(f"""
<div style="
    background: {theme['card_bg']};
    border: 1px solid {theme['card_border']};
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 10px;
    font-size: 0.8rem;
    color: {theme['text_muted']};
">
    📊 Showing <strong style="color: {theme['primary']};">{len(df)}</strong> records for <strong style="color: {theme['text']};">{time_range}</strong>
</div>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown(f"""
<div class="hero-container" style="padding: 24px 28px; margin-bottom: 22px;">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div>
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span class="live-dot"></span>
                <span style="font-size: 0.8rem; font-weight: 700; color: {theme['primary']}; letter-spacing: 0.6px; text-transform: uppercase;">
                    Biometric Telemetry Stream
                </span>
            </div>
            <h1 style="font-size: 2.1rem; font-weight: 800; margin: 0 0 6px 0; color: {theme['text']}; letter-spacing: -0.02em;">
                📊 Primary Health Dashboard
            </h1>
            <div style="font-size: 0.95rem; color: {theme['text_muted']};">
                Monitor your daily biometric indicators, physiological readiness, and trends for <strong style="color:{theme['primary']};">{time_range}</strong>.
            </div>
        </div>
        <div style="
            background: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            border-radius: 12px;
            padding: 10px 16px;
            text-align: right;
        ">
            <div style="font-size: 0.72rem; color: {theme['text_muted']}; text-transform: uppercase; font-weight: 600;">Active Filter</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: {theme['primary']};">{time_range}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)

avg_steps = df['Steps'].mean() if not df.empty else 0
avg_sleep = df['Sleep_Hours'].mean() if not df.empty else 0
avg_hr = df['Heart_Rate_bpm'].mean() if not df.empty else 0
avg_recovery = df['Recovery_Score'].mean() if not df.empty else 0

# Baseline comparisons
step_delta = avg_steps - 10000
sleep_delta = avg_sleep - 7.5
hr_delta = 70.0 - avg_hr  # Lower is generally better

# Step card
with col1:
    step_pct = min(100, int((avg_steps / 10000) * 100))
    step_badge_color = theme['primary'] if avg_steps >= 10000 else theme['accent_amber']
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-label">
            <span>Average Daily Steps</span>
            <span style="font-size: 1.1rem;">👟</span>
        </div>
        <div class="kpi-value">{avg_steps:,.0f}</div>
        <div style="margin: 8px 0 6px 0; background: {theme['card_border']}; height: 5px; border-radius: 9999px; overflow: hidden;">
            <div style="background: {theme['primary_gradient']}; width: {step_pct}%; height: 100%; border-radius: 9999px;"></div>
        </div>
        <div class="kpi-subtitle">
            <span style="color: {step_badge_color}; font-weight: 700;">{step_delta:+,.0f}</span>
            <span>vs 10k Goal ({step_pct}% reached)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sleep card
with col2:
    sleep_pct = min(100, int((avg_sleep / 8.0) * 100))
    sleep_badge_color = theme['primary'] if avg_sleep >= 7.5 else theme['accent_amber']
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-label">
            <span>Average Sleep</span>
            <span style="font-size: 1.1rem;">🌙</span>
        </div>
        <div class="kpi-value">{avg_sleep:.1f} <span style="font-size: 1.1rem; font-weight: 600; color:{theme['text_muted']};">hrs</span></div>
        <div style="margin: 8px 0 6px 0; background: {theme['card_border']}; height: 5px; border-radius: 9999px; overflow: hidden;">
            <div style="background: {theme['secondary_gradient']}; width: {sleep_pct}%; height: 100%; border-radius: 9999px;"></div>
        </div>
        <div class="kpi-subtitle">
            <span style="color: {sleep_badge_color}; font-weight: 700;">{sleep_delta:+.1f}h</span>
            <span>vs 7.5h Target</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Heart Rate card
with col3:
    hr_badge_color = theme['primary'] if avg_hr <= 70 else theme['accent_rose']
    hr_status_text = "Resting Cardiac"
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-label">
            <span>Resting Heart Rate</span>
            <span style="font-size: 1.1rem;">❤️</span>
        </div>
        <div class="kpi-value">{avg_hr:.1f} <span style="font-size: 1.1rem; font-weight: 600; color:{theme['text_muted']};">bpm</span></div>
        <div style="margin: 8px 0 6px 0; background: {theme['card_border']}; height: 5px; border-radius: 9999px; overflow: hidden;">
            <div style="background: {theme['accent_rose']}; width: {min(100, int((avg_hr / 100) * 100))}%; height: 100%; border-radius: 9999px;"></div>
        </div>
        <div class="kpi-subtitle">
            <span style="color: {hr_badge_color}; font-weight: 700;">{hr_delta:+.1f} bpm</span>
            <span>vs 70 bpm standard</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Recovery card
with col4:
    recovery_status = "Optimal" if avg_recovery >= 75 else "Moderate" if avg_recovery >= 55 else "Needs Rest"
    rec_badge_color = theme['primary'] if avg_recovery >= 75 else theme['accent_amber'] if avg_recovery >= 55 else theme['accent_rose']
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-label">
            <span>Mean Recovery Score</span>
            <span style="font-size: 1.1rem;">⚡</span>
        </div>
        <div class="kpi-value" style="color: {rec_badge_color} !important;">
            {avg_recovery:.1f}<span style="font-size: 1.1rem; font-weight: 500; color:{theme['text_muted']};">/100</span>
        </div>
        <div style="margin: 8px 0 6px 0; background: {theme['card_border']}; height: 5px; border-radius: 9999px; overflow: hidden;">
            <div style="background: {theme['primary_gradient']}; width: {min(100, int(avg_recovery))}%; height: 100%; border-radius: 9999px;"></div>
        </div>
        <div class="kpi-subtitle">
            <span style="
                display: inline-block;
                padding: 1px 6px;
                border-radius: 4px;
                background: {rec_badge_color}22;
                color: {rec_badge_color};
                font-weight: 700;
                font-size: 0.72rem;
            ">{recovery_status}</span>
            <span>readiness tier</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PLOTLY CHARTS ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Recovery Score & Sleep Duration Trend")
    
    # Dual-axis line chart using standard subplots
    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

    # Recovery Score Trace
    fig_trend.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Recovery_Score'],
            name="Recovery Score",
            mode='lines+markers',
            line=dict(color=theme['primary'], width=2.8, shape='spline'),
            marker=dict(size=5, symbol="circle"),
            fill='tozeroy',
            fillcolor='rgba(0, 245, 212, 0.06)' if is_dark else 'rgba(0, 150, 136, 0.06)'
        ),
        secondary_y=False
    )

    # Sleep Hours Trace
    fig_trend.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Sleep_Hours'],
            name="Sleep Hours",
            mode='lines+markers',
            line=dict(color=theme['secondary'], width=2.2, dash='dot', shape='spline'),
            marker=dict(size=4)
        ),
        secondary_y=True
    )

    fig_trend.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)"
        )
    )

    fig_trend.update_yaxes(
        title_text="Recovery Score (0-100)",
        range=[0, 105],
        title_font=dict(color=theme['primary'], size=11, family="'Plus Jakarta Sans', sans-serif"),
        tickfont=dict(color=theme['primary'], size=10),
        secondary_y=False
    )

    fig_trend.update_yaxes(
        title_text="Sleep Duration (hrs)",
        range=[3, 11],
        title_font=dict(color=theme['secondary'], size=11, family="'Plus Jakarta Sans', sans-serif"),
        tickfont=dict(color=theme['secondary'], size=10),
        secondary_y=True
    )

    style_plotly_chart(fig_trend)
    st.plotly_chart(fig_trend, use_container_width=True)

with chart_col2:
    st.subheader("🎯 Recovery Score vs. Daily Steps")
    
    fig_scatter = px.scatter(
        df,
        x="Steps",
        y="Recovery_Score",
        color="Heart_Rate_bpm",
        size="Active_Minutes",
        hover_data=["Date", "Sleep_Hours", "Calories_Burned"],
        labels={
            "Steps": "Daily Steps",
            "Recovery_Score": "Recovery Score",
            "Heart_Rate_bpm": "Heart Rate (bpm)",
            "Active_Minutes": "Active Mins"
        },
        color_continuous_scale="Turbo" if is_dark else "Viridis",
        title="Physical Activity Intensity vs Physiological Recovery"
    )
    style_plotly_chart(fig_scatter)
    st.plotly_chart(fig_scatter, use_container_width=True)

# Secondary row of insights
sec_col1, sec_col2 = st.columns(2)

with sec_col1:
    st.subheader("🔥 Daily Energy Expenditure & Active Time")
    fig_energy = px.bar(
        df,
        x="Date",
        y="Calories_Burned",
        color="Active_Minutes",
        color_continuous_scale="Tealgrn" if is_dark else "Mint",
        labels={"Calories_Burned": "Calories Burned (kcal)", "Active_Minutes": "Active Minutes"},
        title="Calories Burned & Active Minutes Distribution"
    )
    style_plotly_chart(fig_energy)
    st.plotly_chart(fig_energy, use_container_width=True)

with sec_col2:
    st.subheader("❤️ Resting Heart Rate Distribution")
    fig_hr = px.histogram(
        df,
        x="Heart_Rate_bpm",
        nbins=15,
        marginal="box",
        color_discrete_sequence=[theme['accent_rose']],
        labels={"Heart_Rate_bpm": "Heart Rate (bpm)"},
        title="Distribution & Spread of Resting Heart Rate"
    )
    style_plotly_chart(fig_hr)
    st.plotly_chart(fig_hr, use_container_width=True)

# --- FILTERED DATA TABLE & DOWNLOAD ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📥 Filtered Records & Telemetry Export")
with st.expander("🔍 Click to view filtered telemetry records", expanded=False):
    st.dataframe(
        df.style.format({
            "Steps": "{:.0f}",
            "Sleep_Hours": "{:.1f}",
            "Heart_Rate_bpm": "{:.1f}",
            "Calories_Burned": "{:.0f}",
            "Active_Minutes": "{:.0f}",
            "Recovery_Score": "{:.0f}"
        }),
        use_container_width=True
    )
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"fitsync_data_{time_range.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown(f"""
<div class="fitsync-footer">
    <strong>FitSync Dashboard</strong> &bull; Biometric Telemetry &bull; Designed & Developed by <strong>FitSync Team</strong>
</div>
""", unsafe_allow_html=True)
