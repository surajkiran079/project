import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import subprocess

def fetch_stock_data(symbol, start_date, end_date, interval):
    stock_data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    return stock_data

def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def candlestick_chart(stock_data):
    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                         open=stock_data['Open'],
                                         high=stock_data['High'],
                                         low=stock_data['Low'],
                                         close=stock_data['Close'])])

    fig.update_layout(title="Candlestick Chart",
                      xaxis_title="Date",
                      yaxis_title="Price",
                      xaxis_rangeslider_visible=False)

    return fig

def rsi_chart(rsi_data):
    fig = go.Figure(go.Scatter(x=rsi_data.index, y=rsi_data, mode='lines', name='RSI', line=dict(color='purple')))
    fig.update_layout(title="ER Indicator",
                      xaxis_title="Date",
                      yaxis_title="ER Indicator",
                      xaxis_rangeslider_visible=False)
    return fig

def main():
    st.title("Candlestick Chart")
    st.subheader("Please fill the Input box to enjoy our tool!")

    # User input for stock symbol, date range, interval, and RSI threshold value
    symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., INFY.NS for Infosys):")
    start_date = st.sidebar.date_input("Select Start Date:")
    end_date = st.sidebar.date_input("Select End Date:", pd.Timestamp.today())
    interval = st.sidebar.selectbox("Select Interval:", ["1d", "1wk", "1mo"])

    # RSI backtesting inputs
    rsi_buying_value = st.sidebar.number_input("Enter ER Value for Buying:")
    execution_date = st.sidebar.date_input("Select Execution Date:")
    stop_loss_percentage = st.sidebar.number_input("Enter Stop Loss Percentage:", min_value=0.0, max_value=100.0, step=0.5, value=2.5)
    target_percentage = st.sidebar.number_input("Enter Target Percentage:", min_value=0.0, max_value=100.0, step=0.5, value=10.0)

    # Fetch stock data
    if symbol:
        try:
            stock_data = fetch_stock_data(symbol, start_date, end_date, interval)
            rsi = calculate_rsi(stock_data)

            # Create candlestick chart
            candlestick_fig = candlestick_chart(stock_data)
            st.plotly_chart(candlestick_fig)

            # Create RSI chart
            rsi_fig = rsi_chart(rsi)
            st.plotly_chart(rsi_fig)

            # RSI backtesting logic
            if rsi_buying_value and execution_date:
                execution_date = pd.to_datetime(execution_date)
                closest_date_idx = rsi.index.get_indexer([execution_date], method='nearest')[0]
                closest_date = rsi.index[closest_date_idx]

                # Calculate stop-loss and target prices
                buying_price = stock_data.loc[closest_date, 'Close']
                stop_loss_price = buying_price * (1 - stop_loss_percentage / 100)
                target_price = buying_price * (1 + target_percentage / 100)

                st.write("Backtesting Results:")
                st.write(f"Execution Date: {closest_date.strftime('%Y-%m-%d')}")
                st.write(f"Buying Price: {buying_price:.2f}")
                st.write(f"Stop Loss Price: {stop_loss_price:.2f}")
                st.write(f"Target Price: {target_price:.2f}")

                # Check if stop-loss or target is hit
                for index, row in stock_data.loc[closest_date:].iterrows():
                    if row['Low'] <= stop_loss_price:
                        st.error("Stop Loss Hit!")
                        break
                    elif row['High'] >= target_price:
                        st.success("Target Hit!")
                        break

        except Exception as e:
            st.error(f"Error fetching stock data: {e}")

if __name__ == "__main__":

    #if st.button("Please Feedback us!"):
        #subprocess.run(["streamlit", "run", "feedback.py"])
    main()