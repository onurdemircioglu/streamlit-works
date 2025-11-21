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
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13 = st.columns(13)

    # Add navigation buttons in the respective columns
    with col1:
        if st.button("Dashboard"):
            navigate_to("page_dashboard")
    
    with col2:
        if st.button("Expense Entry"):
            navigate_to("page_entry")

    with col3:
        if st.button("Reports"):
            navigate_to("page_reports")
    
    with col4:
        if st.button("Reminders"):
            navigate_to("page_reminders")

    with col5:
        if st.button("Latest Entries"):
            navigate_to("page_latest_entries")
    
    with col6:
        if st.button("Settings"):
            navigate_to("page_settings")

    """with col6:
        if st.button("Manage Groups"):
            navigate_to("page_manage_groups")"""
    
    """with col7:
        if st.button("Manage Types"):
            navigate_to("page_types")"""

    """with col8:
        if st.button("Manage Banks"):
            navigate_to("page_banks")"""
    
    with col9:
        if st.button("Calculations"):
            navigate_to("page_calculations")

    with col10:
        if st.button("Exports"):
            navigate_to("page_export")

    with col11:
        if st.button("Change Log"):
            navigate_to("page_changelog")

    with col13:
        if st.button("Test Page"):
            navigate_to("page_test")
            
