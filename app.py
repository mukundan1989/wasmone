import streamlit as st
import yfinance as yf
import pandas as pd
import json
from streamlit_localstorage import LocalStorage

# Set up local storage (WASM IndexedDB)
storage = LocalStorage()

def fetch_stock_data(symbol):
    """Fetch last 10 days of stock price data."""
    stock = yf.Ticker(symbol)
    data = stock.history(period='10d')
    return data[['Close']]

# Streamlit UI
st.title("📈 Stock Price Performance")

symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL):")

if st.button("Get Last 10 Days Performance"):
    if symbol:
        data = fetch_stock_data(symbol)
        if not data.empty:
            st.write(f"### Last 10 Days Closing Prices for {symbol}")
            st.dataframe(data)
            
            # Store in IndexedDB (WASM storage)
            storage.set_item(symbol, data.to_json())
            st.success("Data stored in local storage!")
        else:
            st.error("No data found. Check the stock symbol.")
    else:
        st.warning("Please enter a stock symbol.")

# Fetch stored data if available
stored_keys = storage.keys()
if stored_keys:
    st.write("### Stored Data in Local Storage")
    for key in stored_keys:
        stored_data = storage.get_item(key)
        df = pd.read_json(stored_data)
        st.write(f"#### {key}")
        st.dataframe(df)
