#!/bin/bash
# Salary Prediction Dashboard Startup Script

echo "🎯 Starting Salary Prediction Dashboard..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT" || exit

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

uv run -m streamlit run frontend/streamlit_app.py
