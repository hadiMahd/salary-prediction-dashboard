import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Salary Prediction Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Salary Prediction Dashboard")
st.markdown("---")

st.markdown("""
### Welcome to the Salary Prediction Analytics Platform

This dashboard provides comprehensive insights into salary predictions powered by machine learning 
and enriched with AI narratives.

**📌 Features:**

- **💰 Salaries Analysis**: Explore salary predictions across different experience levels, company sizes, 
and remote work arrangements. View detailed AI narratives for each prediction.

- **📊 Model Performance**: Monitor model metrics, feature importance, and inference times. 
Track model improvements across versions.

---

### 🚀 Getting Started

Select a page from the sidebar to explore:

1. **Salaries Analysis** - Visualize salary distributions and predictions with AI insights
2. **Model Performance** - Review model metrics and performance trends

---

### 📊 What's Inside

**Prediction Data:**
- Job titles and experience levels
- Company information and remote work ratios
- ML model predictions with inference latency
- AI-generated narratives for each prediction

**Model Performance:**
- R² scores, MAE, and RMSE metrics
- Feature importance analysis
- Model version tracking
- Hyperparameter configuration

---

### ⚡ Demo Mode

Currently running with **demo data**. Connect your Supabase instance by setting `SUPABASE_URL` 
and `SUPABASE_KEY` environment variables to use live data.

---

*Last updated: {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}*
""")
