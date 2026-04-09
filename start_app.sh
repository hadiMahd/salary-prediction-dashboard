#!/bin/bash
# Salary Prediction Dashboard Startup Script

echo "🎯 Starting Salary Prediction Dashboard..."
echo ""

cd "$(dirname "$0")" || exit

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first: https://docs.astral.sh/uv/getting-started/"
    exit 1
fi

# Install/sync dependencies
echo "📦 Syncing dependencies..."
uv sync

# Start the app
echo ""
echo "✅ Starting Streamlit app..."
echo "📍 Local URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uv run -m streamlit run streamlit_app.py
