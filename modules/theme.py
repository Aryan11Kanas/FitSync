import streamlit as st

THEME_PALETTES = {
    "dark": {
        "bg": "#090D16",
        "card_bg": "rgba(17, 24, 39, 0.75)",
        "card_border": "rgba(255, 255, 255, 0.08)",
        "card_border_hover": "rgba(0, 245, 212, 0.4)",
        "text": "#F3F4F6",
        "text_muted": "#94A3B8",
        "text_dim": "#64748B",
        "primary": "#00F5D4",
        "primary_glow": "rgba(0, 245, 212, 0.25)",
        "primary_gradient": "linear-gradient(135deg, #00F5D4 0%, #00BBF9 100%)",
        "secondary": "#A855F7",
        "secondary_gradient": "linear-gradient(135deg, #A855F7 0%, #7C3AED 100%)",
        "accent_rose": "#FF3366",
        "accent_amber": "#FFB703",
        "accent_blue": "#38BDF8",
        "grid": "rgba(255, 255, 255, 0.05)",
        "paper_bg": "rgba(10, 15, 26, 0.95)",
        "plot_bg": "rgba(10, 15, 26, 0.85)",
        "hover_bg": "rgba(255, 255, 255, 0.07)",
        "shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
    },
    "light": {
        "bg": "#F4F6FB",
        "card_bg": "rgba(255, 255, 255, 0.88)",
        "card_border": "rgba(226, 232, 240, 0.8)",
        "card_border_hover": "rgba(0, 150, 136, 0.4)",
        "text": "#0F172A",
        "text_muted": "#64748B",
        "text_dim": "#94A3B8",
        "primary": "#009688",
        "primary_glow": "rgba(0, 150, 136, 0.2)",
        "primary_gradient": "linear-gradient(135deg, #009688 0%, #00796B 100%)",
        "secondary": "#7C3AED",
        "secondary_gradient": "linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%)",
        "accent_rose": "#E11D48",
        "accent_amber": "#D97706",
        "accent_blue": "#0284C7",
        "grid": "rgba(0, 0, 0, 0.06)",
        "paper_bg": "#FFFFFF",
        "plot_bg": "#F8FAFC",
        "hover_bg": "rgba(0, 0, 0, 0.04)",
        "shadow": "0 8px 24px 0 rgba(148, 163, 184, 0.15)"
    }
}

def init_theme():
    """Ensure theme state is initialized in Streamlit session_state."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
    return st.session_state["theme"]

def get_current_theme():
    """Return the active theme palette ('dark' or 'light')."""
    theme_name = init_theme()
    return THEME_PALETTES.get(theme_name, THEME_PALETTES["dark"])

def render_sidebar_header():
    """Renders a sleek brand badge at the top of the sidebar."""
    theme = get_current_theme()
    is_dark = st.session_state.get("theme", "dark") == "dark"
    
    st.sidebar.markdown(f"""
    <div style="
        background: {theme['card_bg']};
        border: 1px solid {theme['card_border']};
        border-radius: 14px;
        padding: 16px 14px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: {theme['shadow']};
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 32px;
                    height: 32px;
                    border-radius: 10px;
                    background: {theme['primary_gradient']};
                    color: {'#090D16' if is_dark else '#FFFFFF'};
                    font-size: 1.1rem;
                    font-weight: 800;
                    box-shadow: 0 0 12px {theme['primary_glow']};
                ">⚡</span>
                <span style="font-weight: 800; font-size: 1.25rem; letter-spacing: -0.5px; color: {theme['text']};">
                    Fit<span style="color: {theme['primary']};">Sync</span>
                </span>
            </div>
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 5px;
                padding: 3px 8px;
                background: {theme['primary_glow']};
                border: 1px solid {theme['primary']};
                border-radius: 9999px;
                font-size: 0.68rem;
                font-weight: 700;
                color: {theme['primary']};
                letter-spacing: 0.5px;
            ">
                <span class="live-dot" style="margin: 0; width: 6px; height: 6px;"></span> LIVE
            </span>
        </div>
        <div style="font-size: 0.78rem; color: {theme['text_muted']}; margin-top: 4px;">
            Biometric Telemetry OS • v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_theme_toggle():
    """
    Renders a clean theme toggle button and branding in the sidebar.
    Persists selection in st.session_state['theme'].
    """
    init_theme()
    is_dark = st.session_state["theme"] == "dark"
    label = "☀️ Switch to Light Mode" if is_dark else "🌙 Switch to Dark Mode"

    with st.sidebar:
        st.markdown("---")
        if st.button(label, key="theme_toggle_btn", use_container_width=True):
            st.session_state["theme"] = "light" if is_dark else "dark"
            st.rerun()
            
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 12px 6px 0 6px;
            font-size: 0.74rem;
            color: {get_current_theme()['text_dim']};
        ">
            ⚡ FitSync Team &bull; 2026
        </div>
        """, unsafe_allow_html=True)

def apply_custom_css():
    """
    Injects custom Ultra-Modern Glassmorphic CSS styling matching the active theme into the current page.
    """
    theme = get_current_theme()
    is_dark = st.session_state.get("theme", "dark") == "dark"

    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* Force CSS variables */
        :root {{
            --text-color: {theme['text']} !important;
            --background-color: {theme['bg']} !important;
            --secondary-background-color: {theme['card_bg']} !important;
            --primary-color: {theme['primary']} !important;
        }}

        /* Global Font & Smooth Reset */
        html, body, [class*="css"], .stApp {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            background-color: {theme['bg']} !important;
            color: {theme['text']} !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* Subtle background radial glow in dark mode */
        {"" if not is_dark else f'''
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 20%;
            width: 60%;
            height: 400px;
            background: radial-gradient(circle, rgba(0, 245, 212, 0.04) 0%, rgba(168, 85, 247, 0.03) 50%, transparent 80%);
            pointer-events: none;
            z-index: 0;
        }}
        '''}

        /* Headings & Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: {theme['text']} !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }}

        p, span, label, li, [data-testid="stMarkdownContainer"] p {{
            color: {theme['text']} !important;
            font-feature-settings: "cv02", "cv03", "cv04", "cv11";
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background: {theme['bg']} !important;
            border-right: 1px solid {theme['card_border']} !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebarNav"] span {{
            color: {theme['text']} !important;
        }}

        /* Live Pulsing Dot Animation */
        @keyframes pulse-dot {{
            0% {{
                box-shadow: 0 0 0 0 {theme['primary_glow']};
                opacity: 1;
            }}
            70% {{
                box-shadow: 0 0 0 8px rgba(0, 245, 212, 0);
                opacity: 0.8;
            }}
            100% {{
                box-shadow: 0 0 0 0 rgba(0, 245, 212, 0);
                opacity: 1;
            }}
        }}

        .live-dot {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: {theme['primary']};
            animation: pulse-dot 2s infinite ease-in-out;
            vertical-align: middle;
        }}

        /* Hero Banner Container */
        .hero-container {{
            position: relative;
            background: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            border-radius: 20px;
            padding: 36px 32px;
            margin-bottom: 28px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: {theme['shadow']};
            overflow: hidden;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }}

        .hero-container:hover {{
            border-color: {theme['card_border_hover']};
            box-shadow: 0 12px 40px 0 {theme['primary_glow']};
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: {theme['primary_glow']};
            color: {theme['primary']};
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.6px;
            margin-bottom: 16px;
            border: 1px solid {theme['primary']};
            box-shadow: 0 0 15px {theme['primary_glow']};
        }}

        .hero-title {{
            font-size: 2.6rem;
            font-weight: 800;
            margin: 0 0 12px 0;
            line-height: 1.15;
            letter-spacing: -0.03em;
            background: {'linear-gradient(135deg, #FFFFFF 30%, #A5F3FC 100%)' if is_dark else 'linear-gradient(135deg, #0F172A 30%, #009688 100%)'};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-subtitle {{
            font-size: 1.05rem;
            color: {theme['text_muted']} !important;
            line-height: 1.65;
            margin: 0;
            max-width: 820px;
        }}

        /* Modern KPI Container */
        .kpi-container {{
            position: relative;
            background: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            border-radius: 16px;
            padding: 22px 20px;
            text-align: left;
            margin-bottom: 16px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: {theme['shadow']};
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            overflow: hidden;
        }}

        .kpi-container:hover {{
            transform: translateY(-3px);
            border-color: {theme['card_border_hover']};
            box-shadow: 0 10px 25px -5px {theme['primary_glow']};
        }}

        .kpi-container::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: {theme['primary_gradient']};
            border-radius: 4px 0 0 4px;
        }}

        .kpi-label {{
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: {theme['text_muted']} !important;
            margin-bottom: 6px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .kpi-value {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 2.1rem;
            font-weight: 800;
            color: {theme['text']} !important;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }}

        .kpi-subtitle {{
            font-size: 0.8rem;
            color: {theme['text_muted']} !important;
            margin-top: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* Custom Cards */
        .custom-card {{
            position: relative;
            background: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            border-radius: 18px;
            padding: 24px;
            height: 100%;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: {theme['shadow']};
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .custom-card:hover {{
            transform: translateY(-4px);
            border-color: {theme['card_border_hover']};
            box-shadow: 0 14px 30px -8px {theme['primary_glow']};
        }}

        .card-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: {theme['primary_glow']};
            border: 1px solid {theme['primary']};
            font-size: 1.4rem;
            margin-bottom: 14px;
        }}

        .card-title {{
            font-size: 1.2rem;
            font-weight: 700;
            color: {theme['text']} !important;
            margin: 0 0 10px 0;
            letter-spacing: -0.01em;
        }}

        .card-body {{
            font-size: 0.93rem;
            color: {theme['text_muted']} !important;
            line-height: 1.6;
            margin: 0;
        }}

        /* Step Card */
        .step-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            background: {theme['primary_gradient']};
            color: {'#090D16' if is_dark else '#FFFFFF'} !important;
            font-weight: 800;
            border-radius: 10px;
            margin-right: 12px;
            font-size: 0.95rem;
            box-shadow: 0 0 12px {theme['primary_glow']};
        }}

        /* Streamlit Native Metric cards */
        div[data-testid="stMetric"] {{
            background: {theme['card_bg']} !important;
            border: 1px solid {theme['card_border']} !important;
            border-radius: 16px !important;
            padding: 18px 20px !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            box-shadow: {theme['shadow']} !important;
            transition: all 0.2s ease !important;
        }}

        div[data-testid="stMetric"]:hover {{
            border-color: {theme['card_border_hover']} !important;
            transform: translateY(-2px);
        }}

        div[data-testid="stMetricLabel"] * {{
            color: {theme['text_muted']} !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.6px !important;
        }}

        div[data-testid="stMetricValue"] * {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 2.1rem !important;
            font-weight: 800 !important;
            color: {theme['text']} !important;
            letter-spacing: -0.02em !important;
        }}

        div[data-testid="stMetricDelta"] {{
            font-weight: 600 !important;
            font-size: 0.82rem !important;
        }}

        /* Selectboxes & Dropdowns */
        div[data-baseweb="select"] > div {{
            background-color: {theme['card_bg']} !important;
            border: 1px solid {theme['card_border']} !important;
            border-radius: 12px !important;
            backdrop-filter: blur(10px) !important;
            transition: all 0.2s ease !important;
        }}

        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="select"] > div:focus-within {{
            border-color: {theme['primary']} !important;
            box-shadow: 0 0 0 1px {theme['primary']} !important;
        }}

        div[data-baseweb="select"] * {{
            color: {theme['text']} !important;
            font-weight: 500 !important;
        }}

        /* Expanders */
        div[data-testid="stExpander"] {{
            background-color: {theme['card_bg']} !important;
            border: 1px solid {theme['card_border']} !important;
            border-radius: 14px !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: {theme['shadow']} !important;
            overflow: hidden !important;
        }}

        div[data-testid="stExpander"] summary {{
            padding: 14px 18px !important;
            transition: background 0.2s ease !important;
        }}

        div[data-testid="stExpander"] summary:hover {{
            background: {theme['hover_bg']} !important;
        }}

        div[data-testid="stExpander"] summary span {{
            color: {theme['text']} !important;
            font-weight: 700 !important;
            font-size: 1.02rem !important;
        }}

        /* Buttons */
        div[data-testid="stButton"] > button {{
            background: {theme['card_bg']} !important;
            border: 1px solid {theme['card_border']} !important;
            color: {theme['text']} !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            padding: 10px 18px !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: {theme['shadow']} !important;
        }}

        div[data-testid="stButton"] > button:hover {{
            border-color: {theme['primary']} !important;
            color: {theme['primary']} !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px {theme['primary_glow']} !important;
        }}

        /* Download Button */
        div[data-testid="stDownloadButton"] > button {{
            background: {theme['primary_gradient']} !important;
            color: {'#090D16' if is_dark else '#FFFFFF'} !important;
            border: none !important;
            font-weight: 800 !important;
            border-radius: 12px !important;
            padding: 12px 22px !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 15px {theme['primary_glow']} !important;
        }}

        div[data-testid="stDownloadButton"] > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px {theme['primary_glow']} !important;
            opacity: 0.95 !important;
        }}

        /* Dataframe Modernization */
        div[data-testid="stDataFrame"] {{
            border: 1px solid {theme['card_border']} !important;
            border-radius: 14px !important;
            overflow: hidden !important;
            box-shadow: {theme['shadow']} !important;
        }}

        /* Footer styling */
        .fitsync-footer {{
            text-align: center;
            padding: 24px 0 12px 0;
            border-top: 1px solid {theme['card_border']};
            margin-top: 48px;
            color: {theme['text_muted']};
            font-size: 0.85rem;
        }}

        .fitsync-footer a {{
            color: {theme['primary']} !important;
            text-decoration: none;
            font-weight: 600;
        }}

        .fitsync-footer a:hover {{
            text-decoration: underline;
        }}

        /* Custom Scrollbars */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {theme['bg']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {theme['card_border']};
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {theme['primary']};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    render_sidebar_header()

def style_plotly_chart(fig):
    """
    Applies current theme styling (fonts, grid lines, sleek glass backgrounds)
    to a Plotly Figure instance and returns it.
    """
    theme = get_current_theme()
    is_dark = st.session_state.get("theme", "dark") == "dark"

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif",
            color=theme["text"],
            size=12
        ),
        title=dict(
            font=dict(
                family="'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif",
                color=theme["text"],
                size=16,
                weight=700
            ),
            x=0.01,
            y=0.96
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="'Plus Jakarta Sans', sans-serif",
                color=theme["text"],
                size=11,
                weight=600
            )
        ),
        margin=dict(l=45, r=30, t=55, b=45),
        hoverlabel=dict(
            bgcolor=theme["paper_bg"],
            font_color=theme["text"],
            font_family="'Plus Jakarta Sans', sans-serif",
            font_size=12,
            bordercolor=theme["primary"]
        )
    )

    fig.update_xaxes(
        gridcolor=theme["grid"],
        zerolinecolor=theme["grid"],
        linecolor=theme["card_border"],
        tickfont=dict(
            family="'Plus Jakarta Sans', sans-serif",
            color=theme["text_muted"],
            size=11
        ),
        title_font=dict(
            family="'Plus Jakarta Sans', sans-serif",
            color=theme["text_muted"],
            size=12,
            weight=600
        )
    )
    fig.update_yaxes(
        gridcolor=theme["grid"],
        zerolinecolor=theme["grid"],
        linecolor=theme["card_border"],
        tickfont=dict(
            family="'Plus Jakarta Sans', sans-serif",
            color=theme["text_muted"],
            size=11
        ),
        title_font=dict(
            family="'Plus Jakarta Sans', sans-serif",
            color=theme["text_muted"],
            size=12,
            weight=600
        )
    )

    return fig
