import gradio as gr
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# -----------------------------------------------------
# Placeholder ML model functions (students replace later)
# -----------------------------------------------------

def dummy_predict_price(start_date, end_date, ticker):
    """
    Example placeholder ML function.
    Currently generates random walk time-series.
    Students can replace with real ML model.
    """
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    values = np.cumsum(np.random.randn(len(dates))) + 100  # random walk
    
    df = pd.DataFrame({"Date": dates, "Prediction": values})

    fig = px.line(df, x="Date", y="Prediction", title=f"Dummy Predicted Prices for {ticker}")
    return fig


def dummy_candlestick(start_date, end_date):
    """
    Another placeholder plot (fake candlestick).
    """
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    open_vals = np.random.uniform(90, 110, len(dates))
    close_vals = open_vals + np.random.normal(0, 2, len(dates))
    high_vals = np.maximum(open_vals, close_vals) + np.random.uniform(1, 3, len(dates))
    low_vals = np.minimum(open_vals, close_vals) - np.random.uniform(1, 3, len(dates))

    fig = go.Figure(data=[go.Candlestick(
        x=dates,
        open=open_vals,
        high=high_vals,
        low=low_vals,
        close=close_vals
    )])
    
    fig.update_layout(title="Dummy Candlestick Chart")
    return fig


# -----------------------------------------------------
# Combined function used by Gradio
# -----------------------------------------------------

def run_demo(start_date, end_date, ticker):
    """
    Calls the two placeholder model functions.
    """
    fig1 = dummy_predict_price(start_date, end_date, ticker)
    fig2 = dummy_candlestick(start_date, end_date)
    return fig1, fig2


# -----------------------------------------------------
# Gradio Interface
# -----------------------------------------------------

with gr.Blocks(title="ML Demo App") as demo:
    gr.Markdown("## 📈 ML Model Demo App (Placeholder Version)\n"
                "Enter dates and a stock ticker. The app generates **fake predictions**.\n"
                "Students will later replace the placeholder ML functions.")

    with gr.Row():
        start = gr.Textbox(label="Start Date (YYYY-MM-DD)", placeholder="2025-01-01")
        end   = gr.Textbox(label="End Date (YYYY-MM-DD)", placeholder="2025-02-01")
        tick  = gr.Textbox(label="Ticker", placeholder="AAPL")

    btn = gr.Button("Run Example")

    line_plot = gr.Plot(label="Predicted Line Plot")
    candle_plot = gr.Plot(label="Dummy Candlestick Plot")

    btn.click(run_demo, inputs=[start, end, tick], outputs=[line_plot, candle_plot])


# Run the app
demo.launch()
