import yfinance as yf
import pandas as pd
import streamlit as st
import js  # WebAssembly in Browser

# Set Page Title
st.set_page_config(page_title="Stock Price App", layout="wide")

# Function to fetch stock data
def fetch_stock_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    df = stock.history(period="10d")  # Get last 10 days' data
    df = df[['Close']]  # Keep only the closing price
    df = df.reset_index()
    return df

# Function to store data in WebAssembly (WASM) using Pyodide
def store_in_wasm(stock_symbol, df):
    df_json = df.to_json()
    js.localStorage.setItem(stock_symbol, df_json)  # Store in browser memory

# Function to load from WebAssembly storage
def load_from_wasm(stock_symbol):
    stored_data = js.localStorage.getItem(stock_symbol)
    if stored_data:
        return pd.read_json(stored_data)
    return None

# UI - User Inputs Stock Symbol
st.title("📈 Stock Price Fetcher (Yahoo Finance)")

stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, MSFT)", "AAPL")

if st.button("Fetch & Store Data"):
    stock_data = fetch_stock_data(stock_symbol)
    store_in_wasm(stock_symbol, stock_data)
    st.success(f"Stock Data for {stock_symbol} Stored in Browser!")

if st.button("Show Last 10 Days Performance"):
    stock_data = load_from_wasm(stock_symbol)
    if stock_data is not None:
        st.write(f"📊 Last 10 Days Performance for {stock_symbol}")
        st.dataframe(stock_data)
    else:
        st.warning("No data found! Fetch stock data first.")
