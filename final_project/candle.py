import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from twilio.rest import Client
import webbrowser


st.title("Stocks and ER Indicator values")
st.subheader("Read the Documentation mentioned below before using Platform")
st.subheader("We are not Sebi registered platform,please consult to your financial adviser before Investment or do your own research while investment and backtest the platform")

st.subheader("Follow the Values for investment purpose,these value are Back Tested")
st.subheader("List of stocks and it's Theshold value")

st.subheader("hdfcbnk.ns -  20")
st.subheader("sbin.ns -  21")
st.subheader("kotakbnk.ns -  20")
st.subheader("reliance.ns -  22")
st.subheader("asianpaint.ns -  20")
st.subheader("sail.ns -  20")
st.subheader("coalindia.ns -  20")
st.subheader("bpcl.ns -  22")
st.subheader("tcs.ns -  23")
st.subheader("upl.ns -  23")
st.subheader("srf.ns -  23")



if st.button("main page!"):
    webbrowser.open('https://stock-visualization-forecasting.streamlit.app/')




