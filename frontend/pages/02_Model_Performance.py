import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from lib.utils import fetch_model_performance, format_percentage

st.set_page_config(page_title="Model Performance", page_icon="📊", layout="wide")

st.title("📊 Model Performance Dashboard")

# Fetch data
model_perf_df = fetch_model_performance(use_demo=True)

if model_perf_df.empty:
    st.warning("No model performance data available")
else:
    # Get the latest model for metrics
    latest_model = model_perf_df.iloc[0]
    
    st.subheader("Latest Model Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("R² Score", f"{latest_model['r2_score']:.3f}")
    
    with col2:
        st.metric("MAE", f"${latest_model['mae']:,.2f}")
    
    with col3:
        st.metric("RMSE", f"${latest_model['rmse']:,.2f}")
    
    with col4:
        st.metric("Model Version", latest_model['model_version'])
    
    st.divider()
    
    # Model comparison chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("R² Score Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=model_perf_df["model_version"],
            y=model_perf_df["r2_score"],
            mode="lines+markers",
            marker=dict(size=10, color="steelblue"),
            line=dict(color="steelblue", width=3)
        ))
        fig.update_layout(
            xaxis_title="Model Version",
            yaxis_title="R² Score",
            height=400,
            showlegend=False,
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Error Metrics Comparison")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=model_perf_df["model_version"],
            y=model_perf_df["mae"],
            name="MAE",
            marker_color="lightsalmon"
        ))
        fig.add_trace(go.Bar(
            x=model_perf_df["model_version"],
            y=model_perf_df["rmse"],
            name="RMSE",
            marker_color="lightcoral"
        ))
        fig.update_layout(
            xaxis_title="Model Version",
            yaxis_title="Error Amount ($)",
            height=400,
            barmode="group",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Feature importance
    st.subheader("🎯 Feature Importance (Latest Model)")
    
    feature_importance = latest_model.get("feature_importance", {})
    if feature_importance:
        fi_df = pd.DataFrame(list(feature_importance.items()), columns=["Feature", "Importance"])
        fi_df = fi_df.sort_values("Importance", ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=fi_df["Feature"],
            x=fi_df["Importance"],
            orientation="h",
            marker_color="mediumseagreen"
        ))
        fig.update_layout(
            xaxis_title="Importance Score",
            yaxis_title="Feature",
            height=400,
            showlegend=False,
            hovermode="y unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Hyperparameters
    st.subheader("⚙️ Model Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Latest Model Details**")
        latest_config = latest_model.get("hyperparameters", {})
        
        with st.container(border=True):
            st.write(f"**Algorithm:** {latest_model['algorithm']}")
            st.write(f"**Version:** {latest_model['model_version']}")
            st.write(f"**Training Date:** {latest_model['training_date']}")
            
            if latest_config:
                st.markdown("**Hyperparameters:**")
                for key, value in latest_config.items():
                    st.write(f"- {key}: {value}")
    
    with col2:
        st.markdown("**Model Versions**")
        versions_display = model_perf_df[[
            "model_version", "algorithm", "r2_score", "mae", "rmse"
        ]].copy()
        versions_display.columns = [
            "Version", "Algorithm", "R²", "MAE", "RMSE"
        ]
        versions_display["R²"] = versions_display["R²"].apply(lambda x: f"{x:.3f}")
        versions_display["MAE"] = versions_display["MAE"].apply(lambda x: f"${x:,.2f}")
        versions_display["RMSE"] = versions_display["RMSE"].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(
            versions_display,
            use_container_width=True,
            hide_index=True
        )
    
    st.divider()
    
    # Model narrative
    st.subheader("📝 Model Performance Summary")
    
    narrative = f"""
    The current model (**{latest_model['model_version']}**) using **{latest_model['algorithm']}** 
    achieves an R² score of **{format_percentage(latest_model['r2_score'])}**, explaining 
    {format_percentage(latest_model['r2_score'])} of the variance in salary predictions.
    
    With a Mean Absolute Error (MAE) of **${latest_model['mae']:,.2f}** and Root Mean Squared Error (RMSE) of **${latest_model['rmse']:,.2f}**, 
    the model demonstrates strong predictive accuracy across the salary range.
    
    The most important feature is **Experience Level** at **{format_percentage(feature_importance.get('experience_level', 0))}** importance, 
    followed by **Company Size** at **{format_percentage(feature_importance.get('company_size', 0))}**, 
    indicating that professional experience and organization size are the primary drivers of salary predictions.
    """
    
    st.info(narrative)
