import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from lib.utils import fetch_predictions, format_salary

st.set_page_config(page_title="Salaries Analysis", page_icon="💰", layout="wide")

st.title("💰 Salary Predictions Analysis")

# Fetch data
predictions_df = fetch_predictions(use_demo=True)

if predictions_df.empty:
    st.warning("No prediction data available")
else:
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_salary = predictions_df["predicted_salary"].mean()
        st.metric("Average Salary", format_salary(avg_salary))
    
    with col2:
        max_salary = predictions_df["predicted_salary"].max()
        st.metric("Highest Salary", format_salary(max_salary))
    
    with col3:
        min_salary = predictions_df["predicted_salary"].min()
        st.metric("Lowest Salary", format_salary(min_salary))
    
    with col4:
        total_predictions = len(predictions_df)
        st.metric("Total Predictions", total_predictions)
    
    st.divider()
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Salary by Experience Level")
        salary_by_exp = predictions_df.groupby("experience_level")["predicted_salary"].agg(["mean", "count"])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=salary_by_exp.index,
            y=salary_by_exp["mean"],
            text=[format_salary(x) for x in salary_by_exp["mean"]],
            textposition="auto",
            marker_color="lightblue"
        ))
        fig.update_layout(
            xaxis_title="Experience Level",
            yaxis_title="Average Salary",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Salary Distribution")
        fig = px.box(predictions_df, y="predicted_salary", color_discrete_sequence=["lightcoral"])
        fig.update_layout(height=400, showlegend=False)
        fig.update_yaxes(title="Predicted Salary")
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Salary by company size
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Salary by Company Size")
        salary_by_size = predictions_df.groupby("company_size")["predicted_salary"].mean()
        size_map = {"S": "Small", "M": "Medium", "L": "Large"}
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[size_map.get(x, x) for x in salary_by_size.index],
            y=salary_by_size.values,
            text=[format_salary(x) for x in salary_by_size.values],
            textposition="auto",
            marker_color="lightgreen"
        ))
        fig.update_layout(
            xaxis_title="Company Size",
            yaxis_title="Average Salary",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Remote Ratio Impact")
        salary_by_remote = predictions_df.groupby("remote_ratio")["predicted_salary"].mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=salary_by_remote.index,
            y=salary_by_remote.values,
            mode="lines+markers",
            marker=dict(size=12, color="mediumpurple"),
            line=dict(color="mediumpurple", width=3)
        ))
        fig.update_layout(
            xaxis_title="Remote Ratio (%)",
            yaxis_title="Average Salary",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Detailed predictions table
    st.subheader("📋 Detailed Predictions")
    
    # Create a display dataframe
    display_df = predictions_df[[
        "job_title", "experience_level", "company_size", 
        "remote_ratio", "predicted_salary", "inference_latency_ms"
    ]].copy()
    
    display_df["Experience"] = display_df["experience_level"].map({
        "EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Executive"
    })
    display_df["Company Size"] = display_df["company_size"].map({
        "S": "Small", "M": "Medium", "L": "Large"
    })
    display_df["Remote %"] = display_df["remote_ratio"].astype(str) + "%"
    display_df["Salary"] = display_df["predicted_salary"].apply(format_salary)
    display_df["Latency (ms)"] = display_df["inference_latency_ms"].round(2)
    
    st.dataframe(
        display_df[["job_title", "Experience", "Company Size", "Remote %", "Salary", "Latency (ms)"]],
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    # LLM Narratives
    st.subheader("📝 AI Narratives")
    
    for idx, row in predictions_df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{row['job_title']}**")
                st.caption(f"{row['company_size'].upper()} Company • {row['experience_level']} Level • {row['remote_ratio']}% Remote")
                st.markdown(row['llm_narrative'])
            
            with col2:
                st.metric("💵 Predicted", format_salary(row['predicted_salary']))
