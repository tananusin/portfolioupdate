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
            st.write("DEBUG1:", years_low, pe_25, pe_75)

            if years_low is None:
                st.error("Could not fetch data.")
                return None, None, None

            st.write(f"**Years Low Price:** {years_low:.2f}")

            if pe_25 is not None:
                st.write(f"**25th Percentile P/E:** {pe_25:.2f}")
            else:
                st.write("**25th Percentile P/E:** N/A")

            if pe_75 is not None:
                st.write(f"**75th Percentile P/E:** {pe_75:.2f}")
            else:
                st.write("**75th Percentile P/E:** N/A")

            return years_low, pe_25, pe_75

        else:
            st.info("Click the button to fetch valuation stats.")
            return None, None, None

    except Exception as e:
        st.error(f"Error: {e}")
        st.exception(e)
        return None, None, None
