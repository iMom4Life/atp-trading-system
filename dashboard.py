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
