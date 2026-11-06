# ⚡ FitSync — Personal Health Intelligence Platform

FitSync is a modern, high-performance personal health analytics dashboard built with **Streamlit**, **Pandas**, and **Plotly**. Designed with an Ultra-Modern Dark Glassmorphic interface inspired by WHOOP and Oura, FitSync cleanses wearable biometric telemetry, derives a multi-factor **Recovery Score (0–100)**, and provides interactive exploratory data analysis across sleep, physical activity, and cardiovascular strain.

---

## 🚀 Key Features

* **Glassmorphic Biometric Dashboard:** Interactive KPIs with real-time target progress bars for daily steps, sleep duration, resting heart rate, and composite physical readiness.
* **Algorithmic Recovery Engine:** Multi-factor scoring logic integrating sleep sufficiency, resting cardiac rate, and step distribution into a calibrated 0–100 score.
* **Longitudinal Trends & EDA:** In-depth statistical analysis featuring distribution modeling, day-of-the-week performance breakdowns, monthly progression bars, and Pearson correlation heatmaps.
* **Dynamic Time Filtering:** Instant filtering across *Last 7 Days*, *Last 30 Days*, *Last 90 Days*, and *All Time* with zero-latency cached queries (`@st.cache_data`).
* **Sleek Dual Themes:** Fully responsive Ultra-Modern Dark Mode with ambient glowing accents and a crisp Light Mode toggle.
* **Data Export:** Instant one-click CSV export of filtered biometric datasets.

---

## 📁 Repository Structure

```text
fitsync-project-main/
├── .devcontainer/             # Devcontainer configuration
├── .streamlit/
│   └── config.toml            # Streamlit theme and server configuration
├── data/
│   └── health_data.csv        # Wearable biometric dataset (365 days)
├── modules/
│   ├── processor.py           # Telemetry pipeline: data imputation & recovery scoring
│   └── theme.py               # Theme palettes, glassmorphism CSS & Plotly styling
├── pages/
│   ├── 1_Dashboard.py         # Primary biometric health dashboard
│   └── 2_Trends.py            # Longitudinal trends & advanced EDA
├── tests/
│   └── test_processor.py      # Pytest test suite for processor & scoring logic
├── generate_data.py           # Synthetic telemetry data generator
├── main.py                    # Application landing page & feature showcase
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## ⚡ Quick Start

### 1. Prerequisites & Virtual Environment
Ensure Python 3.10+ is installed. Clone the repository and initialize a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Regenerate Biometric Telemetry
To generate a fresh synthetic dataset:
```bash
python generate_data.py
```

### 4. Launch Application
Run the Streamlit app from the repository root:
```bash
streamlit run main.py
```

Or open specific views directly:
```bash
streamlit run pages/1_Dashboard.py
streamlit run pages/2_Trends.py
```

---

## 🧪 Testing & Validation

Unit tests validate data ingestion, median-based missing value imputation, and physiological recovery score boundary conditions:

```bash
python -m pytest tests/test_processor.py -v
```

Smoke tests can also be run directly:
```bash
python test.py
python test1.py
```

---

## 👥 Credits & Authorship

Designed & Developed with ❤️ by the **FitSync Team**.
