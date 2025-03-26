import streamlit as st
import yfinance as yf
import pandas as pd

# Inject JavaScript for storing and retrieving data in IndexedDB
st.markdown("""
<script>
function saveToLocalStorage(key, value) {
    localStorage.setItem(key, value);
}

function getFromLocalStorage(key) {
    return localStorage.getItem(key);
}
</script>
""", unsafe_allow_html=True)

def fetch_stock_data(symbol):
    """Fetch last 10 days of stock price data."""
    stock = yf.Ticker(symbol)
    data = stock.history(period="10d")
    return data[["Close"]]

st.title("📈 Stock Price Performance (Client-Side)")

symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL):")

if st.button("Get Last 10 Days Performance"):
    if symbol:
        data = fetch_stock_data(symbol)
        if not data.empty:
            st.write(f"### Last 10 Days Closing Prices for {symbol}")
            st.dataframe(data)
            
            # Convert data to JSON for storage
            json_data = data.to_json()
            
            # Store data in IndexedDB using JavaScript
            st.markdown(f"""
            <script>
            saveToLocalStorage("{symbol}", `{json_data}`);
            </script>
            """, unsafe_allow_html=True)

            st.success("Data stored in browser (IndexedDB)!")
        else:
            st.error("No data found. Check the stock symbol.")
    else:
        st.warning("Please enter a stock symbol.")

# Retrieve stored data
st.write("### Stored Data in Browser")
for key in ["AAPL", "GOOGL"]:  # Example stocks
    st.markdown(f"""
    <script>
    let storedData = getFromLocalStorage("{key}");
    if (storedData) {{
        document.write("<h4>{key}</h4>");
        document.write("<pre>" + storedData + "</pre>");
    }}
    </script>
    """, unsafe_allow_html=True)
