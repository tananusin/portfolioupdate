# user_preferences.py
import streamlit as st
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserPreference:
    investment_pct: int
    gold_pct: int
    password: str
    sheet_url: str
    mdd_speculative_pct: int
    mdd_growth_pct: int
    mdd_core_pct: int

    cagr_speculative_pct: Optional[float] = None
    cagr_growth_pct: Optional[float] = None
    cagr_core_pct: Optional[float] = None 
    rebound_speculative_pct: Optional[float] = None
    rebound_growth_pct: Optional[float] = None
    rebound_core_pct: Optional[float] = None

    yield_speculative: Optional[float] = None
    yield_growth: Optional[float] = None
    yield_core: Optional[float] = None 


def convert_to_csv_url(sheet_url: str) -> str:
    sheet_url = sheet_url.strip()
    if "/edit" in sheet_url:
        return sheet_url.split("/edit")[0] + "/export?format=csv"
    elif sheet_url.endswith("/export?format=csv"):
        return sheet_url
    else:
        raise ValueError("Invalid Google Sheet link format.")

def get_user_preferences() -> UserPreference:
    st.sidebar.header("🛠️ User Preference")

    # Google Sheet URL input
    st.sidebar.markdown("### 📄 Google Sheet Source")
    input_url = st.sidebar.text_input(
        label="Enter your Google Sheet URL (optional)",
        placeholder="https://docs.google.com/spreadsheets/d/...",
        help="Leave blank to use the default shared sheet."
    )
    st.sidebar.caption("ℹ️ Paste a shared Google Sheet link ending in `/edit?usp=sharing`.")

    try:
        sheet_url = convert_to_csv_url(input_url) if input_url else st.secrets["google_sheet"]["url"]
    except ValueError:
        st.sidebar.error("❌ Invalid link format. Please make sure it's a shared Google Sheet URL.")
        sheet_url = st.secrets["google_sheet"]["url"]

    st.sidebar.markdown("### 🔑 Switch to Live Data")
    password = st.sidebar.text_input(
        "Enter password for live data access:",
        type="password"
    )

    # Create UserPreference object
    prefs = UserPreference(
        investment_pct=investment_pct,
        gold_pct=gold_pct,
        password=password,
        sheet_url=sheet_url,
        mdd_speculative_pct=mdd_speculative_pct,
        mdd_growth_pct=mdd_growth_pct,
        mdd_core_pct=mdd_core_pct
    )
    
    return prefs

