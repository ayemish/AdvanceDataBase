import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="Flight Price Tracker",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Flight Price Tracker")
st.markdown("Track and monitor flight prices over time")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", [
    "Dashboard",
    "Flights Management", 
    "Price History",
    "Latest Prices"
])

# Helper function to make API calls
def api_get(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def api_post(endpoint, data):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        return response.json() if response.status_code == 200 else None
    except:
        return None

if page == "Dashboard":
    st.header("📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    # Get flights count
    flights = api_get("/flights")
    if flights:
        col1.metric("Total Flights", len(flights))
    else:
        col1.metric("Total Flights", "0")
    
    # Get latest prices count
    latest_prices = api_get("/prices/latest?limit=100")
    if latest_prices:
        col2.metric("Tracked Prices", len(latest_prices.get("latest_prices", [])))
    else:
        col2.metric("Tracked Prices", "0")
    
    col3.metric("API Status", "✅ Online" if flights is not None else "❌ Offline")
    
    # Show recent flights
    if flights:
        st.subheader("Recent Flights")
        flights_df = pd.DataFrame(flights)
        if not flights_df.empty:
            # Select only relevant columns for display
            display_cols = ['flightId', 'airline', 'route', 'flight_date']
            available_cols = [col for col in display_cols if col in flights_df.columns]
            st.dataframe(flights_df[available_cols], use_container_width=True)
    else:
        st.warning("Could not connect to the API. Make sure your FastAPI server is running on http://localhost:8000")

elif page == "Flights Management":
    st.header("🛫 Flights Management")
    
    # Get existing flights
    flights = api_get("/flights")
    
    # Add new flight form
    st.subheader("Add New Flight")
    with st.form("add_flight"):
        col1, col2 = st.columns(2)
        
        with col1:
            flight_id = st.text_input("Flight ID", placeholder="e.g., DL123")
            airline = st.text_input("Airline", placeholder="e.g., Delta Airlines")
            flight_date = st.date_input("Flight Date")
        
        with col2:
            origin = st.text_input("Origin Airport", placeholder="e.g., JFK")
            destination = st.text_input("Destination Airport", placeholder="e.g., LAX")
        
        if st.form_submit_button("Add Flight"):
            if flight_id and airline and origin and destination:
                flight_data = {
                    "flight_id": flight_id,
                    "route": {"from": origin, "to": destination},
                    "airline": airline,
                    "flight_date": flight_date.isoformat()
                }
                result = api_post("/flights", flight_data)
                if result:
                    st.success(f"Flight {flight_id} added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add flight. Check if flight ID already exists.")
            else:
                st.error("Please fill in all fields")
    
    # Display existing flights
    if flights:
        st.subheader("Existing Flights")
        for flight in flights:
            with st.expander(f"🛫 {flight.get('flightId', 'N/A')} - {flight.get('airline', 'N/A')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Route:** {flight.get('route', {}).get('from', 'N/A')} → {flight.get('route', {}).get('to', 'N/A')}")
                    st.write(f"**Date:** {flight.get('flight_date', 'N/A')}")
                with col2:
                    st.write(f"**Flight ID:** {flight.get('flightId', 'N/A')}")
                    if st.button("View Price History", key=f"history_{flight.get('flightId', '')}"):
                        st.session_state.selected_flight = flight.get('flightId')
                        st.switch_page = "Price History"

elif page == "Price History":
    st.header("📈 Price History")
    
    # Flight selector
    flights = api_get("/flights")
    if flights:
        flight_options = {f["flightId"]: f"{f['flightId']} - {f['airline']}" for f in flights}
        selected_flight = st.selectbox("Select Flight", list(flight_options.keys()), 
                                     format_func=lambda x: flight_options[x])
        
        if selected_flight:
            # Get price history
            price_history = api_get(f"/flights/{selected_flight}/prices")
            
            if price_history and price_history.get("prices"):
                prices_df = pd.DataFrame(price_history["prices"])
                prices_df["fetched_at"] = pd.to_datetime(prices_df["fetched_at"])
                
                st.subheader(f"Price History for {selected_flight}")
                
                # Display as table
                st.dataframe(prices_df[["fetched_at", "price", "currency"]], use_container_width=True)
                
                # Simple line chart
                if len(prices_df) > 1:
                    st.subheader("Price Trend")
                    chart_data = prices_df.set_index("fetched_at")[["price"]]
                    st.line_chart(chart_data)
                else:
                    st.info("Not enough data points to show chart")
            else:
                st.warning(f"No price history found for flight {selected_flight}")
                
            # Add new price snapshot
            st.subheader("Add Price Snapshot")
            with st.form("add_price"):
                price = st.number_input("Price", min_value=0.0, step=10.0)
                currency = st.selectbox("Currency", ["USD", "EUR", "GBP"])
                
                if st.form_submit_button("Add Price"):
                    if price > 0:
                        price_data = {
                            "flight_id": selected_flight,
                            "price": price,
                            "currency": currency
                        }
                        result = api_post(f"/flights/{selected_flight}/prices", price_data)
                        if result:
                            st.success("Price snapshot added successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to add price snapshot")
                    else:
                        st.error("Please enter a valid price")
    else:
        st.warning("No flights found. Add some flights first!")

elif page == "Latest Prices":
    st.header("💰 Latest Prices")
    
    limit = st.slider("Number of flights to show", 5, 50, 10)
    
    latest_prices = api_get(f"/prices/latest?limit={limit}")
    
    if latest_prices and latest_prices.get("latest_prices"):
        prices_df = pd.DataFrame(latest_prices["latest_prices"])
        prices_df["fetched_at"] = pd.to_datetime(prices_df["fetched_at"])
        
        # Display table
        st.dataframe(prices_df, use_container_width=True)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Price", f"${prices_df['latest_price'].mean():.2f}")
        col2.metric("Min Price", f"${prices_df['latest_price'].min():.2f}")
        col3.metric("Max Price", f"${prices_df['latest_price'].max():.2f}")
        
    else:
        st.warning("No price data available")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Note:** Make sure your FastAPI server is running on http://localhost:8000")