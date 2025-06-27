import streamlit as st
import pandas as pd

def initialize_session_state():
    """Initializes session state variables for date and time."""
    if "current_year" not in st.session_state:
        st.session_state.current_year = pd.to_datetime('today').year

    if "current_month" not in st.session_state:
        st.session_state.current_month = pd.to_datetime('today').month

    if "current_day" not in st.session_state:
        st.session_state.current_day = pd.to_datetime('today').date()


def display_menu_buttons(navigate_to):
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

    # Add navigation buttons in the respective columns
    with col1:
        if st.button("Home"):
            navigate_to("page_home")
    
    with col2:
        if st.button("Metrics"):
            navigate_to("page_metrics")

    with col3:
        if st.button("Movies"):
            navigate_to("page_movies")

    with col4:
        if st.button("TV Shows"):
            navigate_to("page_tv_shows")
    
    with col5:
        if st.button("Latest Entries"):
            navigate_to("page_latest_entries")
    
    with col6:
        if st.button("Data Entry"):
            navigate_to("page_data_entry")

    with col7:
        if st.button("Update Record"):
            navigate_to("page_update")

    with col8:
        if st.button("Search"):
            navigate_to("page_search")

    with col9:
        if st.button("Test Page"):
            navigate_to("page_test")
            

