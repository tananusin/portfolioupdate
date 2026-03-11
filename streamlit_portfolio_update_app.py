#streamlit_portfolio_update_app.py
import streamlit as st
import pandas as pd

from asset_data import AssetData
from load_assets import load_assets_from_google_sheet
from fetch_data import can_fetch_data, enrich_assets
from portfolio_value import summarize_assets, combine_assets, calculate_portfolio_total, assign_weights
from user_preferences import get_user_preferences, UserPreference
from portfolio_view import get_portfolio_df, show_portfolio_table, show_google_sheet_data_table, show_market_data_table, show_allocation_pie_chart
from pe_percentile import display_valuation_stats


# --- Streamlit Page Config ---
st.set_page_config(page_title="Portfolio Management", layout="centered")
st.title("🗂️ Portfolio")

# --- User Preferences ---
user_pref = get_user_preferences()

# --- Load Asset Data ---
try:
    assets = load_assets_from_google_sheet(user_pref.sheet_url)
except Exception:
    st.error("❌ Failed to load data from the provided Google Sheet. Using default sheet instead.")
    assets = load_assets_from_google_sheet(st.secrets["google_sheet"]["url"])

# --- Check Password and Fetch Live Data ---
if user_pref.password == st.secrets["credentials"]["app_password"]:
    st.success("🔓 Password Correct! Checking live data availability...")

    if can_fetch_data():
        with st.spinner("Fetching live prices and FX rates..."):
            assets = enrich_assets(assets)
    else:
        st.error("❌ Unable to fetch live data. Falling back to static data.")
else:
    st.warning("🔒 Offline Mode: Using static data from Google Sheet.")

# --- For Showing Unsummarized Market Data ---
portfolio_unsum_df = get_portfolio_df(assets)

# --- Portfolio Calculations ---
assets = summarize_assets(assets)
total_thb = calculate_portfolio_total(assets)
current_portfolio_mdd= assign_weights(assets, total_thb)


# --- Convert to DataFrame ---
portfolio_df = get_portfolio_df(assets)

# --- Display Tables ---
tab1, tab2, tab3 = st.tabs(["📋 Portfolio", "📄 Google Sheet", "💹 Market Data"])
with tab1:
    st.subheader("📋 Portfolio Report")
    show_portfolio_table(portfolio_df)
    st.metric("💰 Total Portfolio Value (THB)", f"฿{total_thb:,.0f}")
with tab2:
    st.subheader("📄 Google Sheet Format")
    show_google_sheet_data_table(portfolio_df)
with tab3:
    st.subheader("💹 Market Data")
    st.caption("ℹ️ Fetchable data. When using live data mode, copy this data to your Google Sheet to update static data.")
    show_market_data_table(portfolio_unsum_df)
    st.subheader("🧮 Years Low Price and P/E Ratio Percentiles")
    symbol = st.text_input("Enter stock symbol (e.g., AAPL)", value="AAPL")

    if user_pref.password == st.secrets["credentials"]["app_password"]:
        st.success("🔓 Password Correct! Checking live data availability...")
        if can_fetch_data():  # ✅ Check fetch readiness
            with st.spinner("Fetching data OK"):
                years_low, pe_p25, pe_p75 = display_valuation_stats(symbol)
        else:
            st.error("❌ Unable to fetch live data. Falling back to static data.")
    else:
        st.warning("🔒 Offline Mode: Available only for online mode.")


# --- Display Pie Charts ---
assets_combine = combine_assets(assets)
portfolio_combine_df = get_portfolio_df(assets_combine)

st.subheader("📊 Allocation Pie Chart")
show_allocation_pie_chart(portfolio_combine_df, total_thb)



