import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.processor import process_data
from modules.theme import init_theme, render_theme_toggle, apply_custom_css, style_plotly_chart, get_current_theme

# Page Configuration
st.set_page_config(
    page_title="FitSync — Trends & Analytics",
    page_icon="📈",
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
    Loads and caches processed health data for fast page switching.
    """
    return process_data()

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
        🔍 Statistical Scope
    </div>
</div>
""", unsafe_allow_html=True)

time_range = st.sidebar.selectbox(
    "Select Time Window",
    options=["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
    index=3  # Default to All Time for macro statistical trends
)

# Copy dataframe before applying filter
filtered_df = full_df.copy()
if 'Date' in filtered_df.columns and not filtered_df.empty:
    max_date = filtered_df['Date'].max()
    if time_range == "Last 7 Days":
        filtered_df = filtered_df[filtered_df['Date'] >= (max_date - pd.Timedelta(days=7))].copy()
    elif time_range == "Last 30 Days":
        filtered_df = filtered_df[filtered_df['Date'] >= (max_date - pd.Timedelta(days=30))].copy()
    elif time_range == "Last 90 Days":
        filtered_df = filtered_df[filtered_df['Date'] >= (max_date - pd.Timedelta(days=90))].copy()

    filtered_df = filtered_df.sort_values('Date').reset_index(drop=True)

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
    📈 Analyzing <strong style="color: {theme['primary']};">{len(filtered_df)}</strong> days of continuous records
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
                    Longitudinal Analytics & EDA
                </span>
            </div>
            <h1 style="font-size: 2.1rem; font-weight: 800; margin: 0 0 6px 0; color: {theme['text']}; letter-spacing: -0.02em;">
                📈 Statistical Trends & Biometric Modeling
            </h1>
            <div style="font-size: 0.95rem; color: {theme['text_muted']};">
                In-depth exploratory data analysis, parameter distributions, and correlation matrices for <strong style="color:{theme['primary']};">{time_range}</strong>.
            </div>
        </div>
        <div style="
            background: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            border-radius: 12px;
            padding: 10px 16px;
            text-align: right;
        ">
            <div style="font-size: 0.72rem; color: {theme['text_muted']}; text-transform: uppercase; font-weight: 600;">Data Horizon</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: {theme['primary']};">{time_range}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SUMMARY STATISTICS SECTION ---
st.subheader("📊 Parametric Summary Statistics")
summary_cols = ['Steps', 'Sleep_Hours', 'Heart_Rate_bpm', 'Calories_Burned', 'Active_Minutes', 'Recovery_Score']
valid_summary_cols = [c for c in summary_cols if c in filtered_df.columns]

if not filtered_df.empty and valid_summary_cols:
    stats_df = filtered_df[valid_summary_cols].describe().T
    stats_df = stats_df[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]
    st.dataframe(
        stats_df.style.format({
            'count': '{:.0f}',
            'mean': '{:.1f}',
            'std': '{:.1f}',
            'min': '{:.1f}',
            '25%': '{:.1f}',
            '50%': '{:.1f}',
            '75%': '{:.1f}',
            'max': '{:.1f}'
        }),
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- DISTRIBUTIONS SECTION ---
st.subheader("📊 Metric Distributions & Spread")
col_dist1, col_dist2 = st.columns(2)

with col_dist1:
    fig_steps = px.histogram(
        filtered_df,
        x="Steps",
        nbins=20,
        marginal="rug",
        color_discrete_sequence=[theme['primary']],
        title="Distribution of Daily Step Counts",
        labels={"Steps": "Daily Steps"}
    )
    # Add mean line
    mean_steps = filtered_df['Steps'].mean()
    fig_steps.add_vline(
        x=mean_steps,
        line_dash="dash",
        line_color=theme['secondary'],
        line_width=2.5,
        annotation_text=f"Mean: {mean_steps:,.0f}",
        annotation_position="top right",
        annotation_font=dict(color=theme['secondary'], family="'Plus Jakarta Sans', sans-serif", weight=700)
    )
    style_plotly_chart(fig_steps)
    st.plotly_chart(fig_steps, use_container_width=True)

with col_dist2:
    fig_cal = px.histogram(
        filtered_df,
        x="Calories_Burned",
        nbins=20,
        marginal="rug",
        color_discrete_sequence=[theme['secondary']],
        title="Distribution of Calories Burned (kcal)",
        labels={"Calories_Burned": "Calories Burned (kcal)"}
    )
    mean_cal = filtered_df['Calories_Burned'].mean()
    fig_cal.add_vline(
        x=mean_cal,
        line_dash="dash",
        line_color=theme['primary'],
        line_width=2.5,
        annotation_text=f"Mean: {mean_cal:,.0f} kcal",
        annotation_position="top right",
        annotation_font=dict(color=theme['primary'], family="'Plus Jakarta Sans', sans-serif", weight=700)
    )
    style_plotly_chart(fig_cal)
    st.plotly_chart(fig_cal, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- LONGITUDINAL TRENDS & AGGREGATIONS ---
col_trend1, col_trend2 = st.columns(2)

with col_trend1:
    st.subheader("😴 Sleep Duration Longitudinal Trend")
    fig_sleep = px.line(
        filtered_df,
        x="Date",
        y="Sleep_Hours",
        title="Daily Sleep Duration Over Time",
        markers=True,
        labels={"Sleep_Hours": "Sleep Duration (hrs)", "Date": "Date"}
    )
    fig_sleep.update_traces(
        line=dict(color=theme['primary'], width=2.5, shape='spline'),
        marker=dict(size=4.5)
    )
    # Baseline benchmark line
    fig_sleep.add_hline(
        y=7.0,
        line_dash="dash",
        line_color=theme['accent_rose'],
        line_width=2,
        annotation_text="7.0h Baseline",
        annotation_position="bottom right",
        annotation_font=dict(color=theme['accent_rose'], family="'Plus Jakarta Sans', sans-serif", weight=700)
    )
    style_plotly_chart(fig_sleep)
    st.plotly_chart(fig_sleep, use_container_width=True)

with col_trend2:
    st.subheader("🗓️ Average Recovery Score by Month")
    if 'Date' in filtered_df.columns and len(filtered_df) > 1:
        # String conversion to prevent JSON serialization errors
        trend_copy = filtered_df.copy()
        trend_copy["Month"] = trend_copy["Date"].dt.to_period("M").astype(str)
        monthly_avg = (
            trend_copy.groupby("Month")["Recovery_Score"]
            .mean()
            .reset_index()
        )
        fig_month = px.bar(
            monthly_avg,
            x="Month",
            y="Recovery_Score",
            title="Monthly Mean Recovery Score Progression",
            text_auto=".1f",
            color="Recovery_Score",
            color_continuous_scale="Tealgrn" if is_dark else "Viridis",
            labels={"Recovery_Score": "Mean Recovery", "Month": "Month"}
        )
        fig_month.update_traces(
            textposition='outside',
            textfont=dict(family="'Plus Jakarta Sans', sans-serif", weight=700)
        )
        style_plotly_chart(fig_month)
        st.plotly_chart(fig_month, use_container_width=True)
    else:
        st.info("Insufficient date span for monthly breakdown.")

st.markdown("<br>", unsafe_allow_html=True)

# --- ADVANCED STATISTICAL INSIGHTS ---
col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    st.subheader("🔥 Metric Correlation Heatmap")
    corr_cols = [c for c in ['Steps', 'Sleep_Hours', 'Heart_Rate_bpm', 'Calories_Burned', 'Active_Minutes', 'Recovery_Score'] if c in filtered_df.columns]
    if len(corr_cols) > 1 and len(filtered_df) > 2:
        corr_matrix = filtered_df[corr_cols].corr()
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="Pearson Correlation Matrix (Linear Associations)",
            labels=dict(color="Correlation")
        )
        fig_corr.update_traces(
            textfont=dict(family="'Plus Jakarta Sans', sans-serif", size=11, weight=600)
        )
        style_plotly_chart(fig_corr)
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Not enough data points for correlation matrix.")

with col_stat2:
    st.subheader("📅 Day of the Week Performance")
    if 'Date' in filtered_df.columns and len(filtered_df) >= 7:
        dow_df = filtered_df.copy()
        dow_df['Day_of_Week'] = dow_df['Date'].dt.day_name()
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_avg = dow_df.groupby('Day_of_Week')[['Steps', 'Recovery_Score']].mean().reindex(days_order).reset_index()
        
        fig_dow = go.Figure()
        fig_dow.add_trace(go.Bar(
            x=dow_avg['Day_of_Week'],
            y=dow_avg['Recovery_Score'],
            name="Mean Recovery Score",
            marker=dict(
                color=dow_avg['Recovery_Score'],
                colorscale="Viridis",
                showscale=False
            ),
            text=dow_avg['Recovery_Score'].round(1),
            textposition='outside',
            textfont=dict(family="'Plus Jakarta Sans', sans-serif", weight=700)
        ))
        fig_dow.update_layout(
            title="Mean Recovery Score by Day of Week",
            xaxis_title="Day of Week",
            yaxis_title="Recovery Score (0-100)",
            yaxis=dict(range=[0, 105])
        )
        style_plotly_chart(fig_dow)
        st.plotly_chart(fig_dow, use_container_width=True)
    else:
        st.info("Need at least 7 days of data for day-of-week breakdown.")

# Footer
st.markdown(f"""
<div class="fitsync-footer">
    <strong>FitSync Analytics</strong> &bull; Longitudinal Trends & Statistical Modeling &bull; Designed & Developed by <strong>FitSync Team</strong>
</div>
""", unsafe_allow_html=True)
