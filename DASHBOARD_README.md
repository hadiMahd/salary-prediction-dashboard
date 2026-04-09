# 🎯 Salary Prediction Dashboard

A Streamlit application for analyzing salary predictions from an ML model with AI-generated narratives and model performance metrics.

## ✨ Features

### 💰 Salaries Analysis Page
- **Summary Metrics**: Average, highest, and lowest salaries at a glance
- **Salary Visualizations**:
  - Salary distribution by experience level
  - Overall salary distribution box plot
  - Salary by company size comparison
  - Remote work impact on salary analysis
- **Detailed Predictions Table**: Browse all predictions with job titles, experience levels, and inference times
- **AI Narratives**: LLM-generated insights for each prediction

### 📊 Model Performance Page
- **Key Metrics**: R² score, MAE, RMSE, and model version
- **Performance Trends**: 
  - R² score evolution across model versions
  - Error metrics (MAE & RMSE) comparison
- **Feature Importance**: Interactive chart showing feature contribution to predictions
- **Model Configuration**: Hyperparameters and training details for each model version
- **Performance Summary**: AI-generated narrative about model accuracy and key drivers

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- uv package manager

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Run the app:
```bash
uv run -m streamlit run streamlit_app.py
```

3. Open your browser and navigate to `http://localhost:8501`

## 📊 Demo Mode

The app runs with **hardcoded demo data** by default. This includes:
- 4 sample salary predictions with varying experience levels
- 2 model performance records with different metrics

No Supabase connection required to run the demo!

## 🔗 Connect to Supabase (Optional)

To use live data from Supabase:

1. Set environment variables:
```bash
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"
```

2. Update the app to fetch real data by changing `use_demo=True` to `use_demo=False` in:
   - `pages/01_Salaries_Analysis.py`
   - `pages/02_Model_Performance.py`

The app will gracefully fall back to demo data if Supabase is unavailable.

## 📁 Project Structure

```
.
├── streamlit_app.py              # Main application entry point
├── pages/
│   ├── 01_Salaries_Analysis.py  # Salary predictions dashboard
│   └── 02_Model_Performance.py  # Model metrics dashboard
├── lib/
│   ├── __init__.py
│   └── utils.py                  # Supabase connection & demo data
├── .streamlit/
│   └── config.toml               # Streamlit UI configuration
├── db_schema.sql                 # PostgreSQL schema
└── pyproject.toml                # Project dependencies
```

## 🗄️ Data Schema

### Predictions Table
- Salary predictions with job details
- LLM narratives explaining predictions
- Chart data for visualization
- Inference latency metrics

### Model Performance Table
- Model version and algorithm
- Performance metrics (R², MAE, RMSE)
- Feature importance scores
- Hyperparameters and training date

## 🎨 UI/UX

- Clean, professional design with Plotly interactive charts
- Responsive grid layout
- Color-coded visualizations
- Mobile-friendly on smaller screens
- Summary cards for key metrics

## 🧠 Technology Stack

- **Streamlit**: Web app framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **Supabase**: PostgreSQL database
- **Python 3.12+**: Runtime

## 📝 Notes

- All visualizations are interactive (hover for details, zoom, pan)
- Data updates require app restart (hardcoded demo) or Supabase refresh
- AI narratives are pre-generated and stored with predictions

## 🔧 Development

To modify the demo data, edit `lib/utils.py`:
- `DEMO_PREDICTIONS`: Sample salary predictions
- `DEMO_MODEL_PERFORMANCE`: Sample model metrics

## 📄 License

MIT
