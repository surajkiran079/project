import streamlit as st

def main_page():
    st.title("Stocks and ER Indicator Values")
    st.subheader("Read the Documentation mentioned below before using the Platform")
    st.subheader("We are not a SEBI registered platform. Please consult your financial adviser before investment or do your own research while investing and backtest the platform.")

    st.write("""
    ### Follow the Values for Investment Purpose
    These values are backtested. However, always ensure to perform your own due diligence.
    """)

    st.write("""
    ### List of Stocks and Their Threshold Values
    - **hdfcbnk.ns** - 20
    - **sbin.ns** - 21
    - **kotakbnk.ns** - 20
    - **reliance.ns** - 22
    - **asianpaint.ns** - 20
    - **sail.ns** - 20
    - **coalindia.ns** - 20
    - **bpcl.ns** - 22
    - **tcs.ns** - 23
    - **upl.ns** - 23
    - **srf.ns** - 23
    """)

def stocks_page():
    stocks.main()

def virtual_tradings():
    virtual_trading.main()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main Page", "Stocks Page"])

main_page()


