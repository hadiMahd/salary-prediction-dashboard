# 🚀 Salary Prediction Dashboard - Setup Guide

## ✅ What's Been Created

Your Streamlit dashboard is ready to run with **demo data** (no Supabase connection needed!). Here's what you have:

### 📦 Project Structure
```
assig-1/
├── streamlit_app.py               👈 Main dashboard entry point
├── pages/
│   ├── 01_Salaries_Analysis.py    💰 Salary predictions & analysis
│   └── 02_Model_Performance.py    📊 Model metrics dashboard
├── lib/
│   ├── __init__.py
│   └── utils.py                    🔌 Supabase connection + demo data
├── .streamlit/
│   └── config.toml                 ⚙️ UI configuration
├── start_app.sh                    🎬 Quick start script
└── DASHBOARD_README.md             📖 Full documentation
```

## 🎬 How to Run

### Option 1: Using the startup script (Recommended) ⭐
```bash
./start_app.sh
```

### Option 2: Manual startup
```bash
uv sync
uv run -m streamlit run streamlit_app.py
```

The app will start at: **http://localhost:8501**

## 📊 Dashboard Pages

### 💰 Salaries Analysis (Page 1)
- Summary metrics (Average, Highest, Lowest salaries)
- Interactive charts:
  - Salary by experience level
  - Salary distribution
  - Salary by company size
  - Remote work impact
- Detailed predictions table
- AI narratives for each prediction

### 📊 Model Performance (Page 2)
- Model metrics: R², MAE, RMSE
- Performance trends across versions
- Feature importance analysis
- Model configuration & hyperparameters
- Model performance summary narrative

## 🔄 Connecting to Supabase (Optional)

To use live data instead of demo data:

1. **Set environment variables:**
   ```bash
   export SUPABASE_URL="your_url_here"
   export SUPABASE_KEY="your_key_here"
   ```

2. **Update the pages to fetch real data:**
   - Edit `pages/01_Salaries_Analysis.py` 
   - Change `fetch_predictions(use_demo=True)` to `fetch_predictions(use_demo=False)`
   - Repeat for `pages/02_Model_Performance.py`

3. **The app will:**
   - Try to connect to Supabase
   - Automatically fall back to demo data if connection fails
   - Display your real data if connection succeeds

## 📝 Demo Data Included

The app comes with realistic sample data:

**4 Salary Predictions:**
- Senior Data Scientist ($152,000)
- ML Engineer ($125,000)
- Director of Data Science ($210,000)
- Junior Data Analyst ($65,000)

**2 Model Versions:**
- v1.0.0: R² score 0.892
- v1.1.0: R² score 0.905

All with sample narratives and charts!

## 🧪 Testing the App

The app was verified and is working! You should see:
- ✅ Home page with dashboard overview
- ✅ Salaries Analysis page with charts and narratives
- ✅ Model Performance page with metrics

## 💡 Customizing Demo Data

To modify demo data, edit `lib/utils.py`:

```python
DEMO_PREDICTIONS = [
    {
        "id": "1",
        "job_title": "Your Job Title",
        "predicted_salary": 150000,
        "llm_narrative": "Your custom narrative here",
        # ... more fields
    },
    # Add more predictions
]

DEMO_MODEL_PERFORMANCE = [
    # Add model versions
]
```

## 🎨 UI Customization

Modify Streamlit theme in `.streamlit/config.toml`:
- Colors, fonts, layout
- Server settings
- Logger levels

## 📚 Technology Stack

- **Streamlit** - Web app framework
- **Plotly** - Interactive charts
- **Pandas** - Data manipulation
- **Supabase** - PostgreSQL database (optional)
- **Python 3.12+** - Runtime

## 🔗 Database Schema

The app aligns with your `db_schema.sql`:

**Predictions Table:**
- Salary predictions with job details
- LLM narratives
- Chart data
- Inference latency

**Model Performance Table:**
- Model versions & algorithms
- Performance metrics (R², MAE, RMSE)
- Feature importance
- Hyperparameters

## ❓ Troubleshooting

**App won't start:**
- Run `uv sync` to ensure dependencies are installed
- Check Python version: `python3 --version` (needs 3.12+)

**Import errors:**
- Ensure you're in the correct directory
- Run `uv sync` again

**Charts not showing:**
- Plotly may need to be reinstalled: `uv pip install --upgrade plotly`

**Demo data not appearing:**
- Check `lib/utils.py` has DEMO_PREDICTIONS data
- Verify imports in page files

## 📖 Full Documentation

See `DASHBOARD_README.md` for comprehensive documentation.

---

**You're all set!** 🎉 Run `./start_app.sh` to launch your dashboard.
