# pe_percentile.py
import streamlit as st
from fetch_data import valuation_stats

def display_valuation_stats(symbol: str):
    try:
        months = st.number_input("How many months?", min_value=6, max_value=60, value=36, step=6)

        # Add button to trigger fetch
        if st.button("Fetch P/E Percentiles"):
            years_low, pe_25, pe_75 = valuation_stats(symbol, months)

            if pe_25 is None or pe_75 is None:
                st.error("Could not compute percentiles.")
            else:
                st.write(f"**25th Percentile P/E:** {pe_25:.2f}")
                st.write(f"**75th Percentile P/E:** {pe_75:.2f}")
            
            return years_low, pe_25, pe_75
        else:
            st.info("Click the button to fetch P/E percentiles.")
            return None, None

    except Exception:
        return None, None
