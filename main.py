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
