import streamlit as st
import yfinance as yf
import pandas as pd

# JavaScript to store and retrieve data from IndexedDB (via localStorage)
st.markdown("""
<script>
function saveToLocalStorage(key, value) {
    localStorage.setItem(key, value);
}

function getFromLocalStorage(key) {
    return localStorage.getItem(key);
}

// Function to send stored data to Streamlit
function sendStoredDataToStreamlit() {
    let storedData = {};
    for (let i = 0; i < localStorage.length; i++) {
        let key = localStorage.key(i);
        storedData[key] = localStorage.getItem(key);
    }
    // Send data to Streamlit
    window.parent.postMessage(storedData, "*");
}

// Run function after page loads
setTimeout(sendStoredDataToStreamlit, 1000);
</script>
""", unsafe_allow_html=True)

# Title
st.title("📈 Stock Price Performance (Client-Side)")

# Input stock symbol
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL):")

def fetch_stock_data(symbol):
    """Fetch last 10 days of stock price data."""
    stock = yf.Ticker(symbol)
    data = stock.history(period="10d")
    return data[["Close"]]

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

# Section to display stored data
st.write("### Stored Data in Browser")

# Capture IndexedDB data using Streamlit session state
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

# Streamlit listens for messages from JavaScript
st.markdown("""
<script>
window.addEventListener("message", (event) => {
    const storedData = event.data;
    if (storedData) {
        fetch("/_stcore_update_session_state", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ stored_data: storedData })
        });
    }
});
</script>
""", unsafe_allow_html=True)

# Display stored data
if st.session_state.stored_data:
    for stock, json_data in st.session_state.stored_data.items():
        st.write(f"**{stock}**")
        st.json(json_data)
else:
    st.info("No data found in IndexedDB.")
