import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from twilio.rest import Client
import subprocess
import register

def fetch_stock_data(symbol, period, interval):
    stock_data = yf.download(symbol, period=period, interval=interval)
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

def send_sms(receiver_phone_number, symbol, rsi_value):
    account_sid = 'ACbe2dd60b96c757b5dc4cb2557489fc6b'
    auth_token = '26430d7584d6fbc5df1aa0f81612ce93'
    client = Client(account_sid, auth_token)
    message = client.messages.create(

        body=f"{symbol} has crossed the ER threshold of {rsi_value}.",
        from_='+14243527186',# remove the zeros
        to=receiver_phone_number
    )
    return message.sid

def main():
    st.title("Stock Chart with ER Indicator")
    st.subheader("Please fill the Input box to enjoy our tool!")

    # User input for stock symbol, period, interval, and RSI threshold value
    symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., INFY.NS for Infosys):")
    period = st.sidebar.selectbox("Select Period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y","10y"])
    interval = st.sidebar.selectbox("Select Interval:", ["1d", "1wk", "1mo"])
    rsi_value = st.sidebar.number_input("Enter ER Threshold Value:", min_value=20)

    # User input for SMS notification
    receiver_phone_number = st.sidebar.text_input("Enter your phone number for SMS notifications:")

    # Fetch stock data
    if symbol:
        try:
            stock_data = fetch_stock_data(symbol, period, interval)
            rsi = calculate_rsi(stock_data)

            # Create candlestick chart
            candlestick_fig = candlestick_chart(stock_data)
            st.plotly_chart(candlestick_fig)

            # Create RSI chart
            rsi_fig = rsi_chart(rsi)
            st.plotly_chart(rsi_fig)

            # Check if RSI crosses threshold and send SMS notification
            if rsi.iloc[-1] > rsi_value and receiver_phone_number:
                send_sms(receiver_phone_number, symbol, rsi.iloc[-1])
                st.success("SMS notification sent!")

        except Exception as e:
            st.error(f"Error fetching stock data: {e}")



if __name__ == "__main__":

    if st.button("Backtest-us !"):
        subprocess.run(["streamlit", "run", "virtual_trading.py"])
    if st.button("Please Feedback us!"):
        subprocess.run(["streamlit", "run", "feedback.py"])
    main()


