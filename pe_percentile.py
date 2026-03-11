# pe_percentile.py
import streamlit as st
from fetch_data import valuation_stats

def display_valuation_stats(symbol: str):
    try:
        months = st.number_input(
            "How many months?",
            min_value=6,
            max_value=60,
            value=36,
            step=6
        )

        if st.button("Fetch Valuation Stats"):

            years_low, pe_25, pe_75 = valuation_stats(symbol, months)

            if years_low is None:
                st.error("Could not fetch data.")
                return None, None, None

            return years_low, pe_25, pe_75

        else:
            st.info("Click the button to fetch valuation stats.")
            return None, None, None

    except Exception:
        return None, None, None
