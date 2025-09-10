# main.py - FastAPI wrapper for testing
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="ATP v3.0 API", version="3.0.0")

# Allow frontend to connect to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/start_session")
async def start_session(params: dict = Body(...)):
    """Start a new trading session"""
    return {"status": "success", "session_id": "test_session_123", "params": params}

@app.post("/add_analysis")
async def add_analysis(ticker: str, data: dict = Body(...)):
    """Add analysis result for a ticker"""
    return {"id": 1, "ticker": ticker, "status": "added", "data": data}

@app.post("/record_outcome")
async def record_outcome(analysis_id: int, outcome: str, exit_price: float = None, notes: str = None):
    """Record trade outcome"""
    return {"success": True, "analysis_id": analysis_id, "outcome": outcome}

@app.get("/performance_metrics")
async def get_metrics():
    """Get performance metrics"""
    return {
        "win_rate": 63.4,
        "expectancy": 1.7,
        "profit_factor": 2.2,
        "total_trades": 82,
        "average_win": 2.1,
        "average_loss": -1.3,
        "max_drawdown": -6.8,
        "sharpe_ratio": 1.5
    }

@app.get("/trade_history")
async def trade_history(limit: int = 100):
    """Get trade history"""
    return [
        {"ticker": "AAPL", "timestamp": "2024-12-19T10:30:00", "confidence_score": 8.7, 
         "outcome_status": "HIT_TARGET", "pnl": 5.0},
        {"ticker": "MSFT", "timestamp": "2024-12-19T11:15:00", "confidence_score": 9.1,
         "outcome_status": "HIT_SECONDARY", "pnl": 9.85},
        {"ticker": "TSLA", "timestamp": "2024-12-19T12:00:00", "confidence_score": 6.5,
         "outcome_status": "STOPPED_OUT", "pnl": -5.3}
    ]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "3.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOFcat > dashboard.py << 'EOF'
# dashboard.py - ATP v3.0 Trading Dashboard
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

API_BASE_URL = "http://localhost:8000"
st.set_page_config(page_title="ATP v3.0 Trading Dashboard", layout="wide")
st.title("🎯 ATP v3.0 Trading Dashboard")

# Check backend connection
try:
    health = requests.get(f"{API_BASE_URL}/health", timeout=5)
    if health.status_code == 200:
        st.success("✅ Connected to backend API")
    else:
        st.error("❌ Backend not responding")
except:
    st.error("❌ Cannot connect to backend. Make sure to run: uvicorn main:app --reload --port 8000")

# Sidebar
with st.sidebar:
    st.header("Session Management")
    if st.button("🔄 Refresh Data"):
        st.rerun()

# Main content
tab1, tab2, tab3 = st.tabs(["📊 Performance", "📈 Charts", "📋 Trade History"])

with tab1:
    st.header("Performance Metrics")
    try:
        metrics = requests.get(f"{API_BASE_URL}/performance_metrics").json()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Win Rate", f"{metrics.get('win_rate', 0)}%")
        col2.metric("Expectancy", f"${metrics.get('expectancy', 0):.2f}")
        col3.metric("Profit Factor", f"{metrics.get('profit_factor', 0):.2f}")
        col4.metric("Total Trades", metrics.get('total_trades', 0))
    except:
        st.info("No performance data yet. Record some trades first!")

with tab2:
    st.header("Equity Curve")
    try:
        trades = requests.get(f"{API_BASE_URL}/trade_history?limit=100").json()
        if trades:
            df = pd.DataFrame(trades)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            df['cumulative_pnl'] = df['pnl'].cumsum()
            
            fig = px.line(df, x='timestamp', y='cumulative_pnl', title="Cumulative PnL")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trades recorded yet")
    except:
        st.info("Could not load trade data")

with tab3:
    st.header("Trade History")
    try:
        trades = requests.get(f"{API_BASE_URL}/trade_history?limit=50").json()
        if trades:
            df = pd.DataFrame(trades)
            st.dataframe(df[['ticker', 'timestamp', 'confidence_score', 'outcome_status', 'pnl']])
        else:
            st.info("No trades recorded yet")
    except:
        st.info("Could not load trade history")
