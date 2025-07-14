import streamlit as st

st.set_page_config(page_title="Personal Finance Assistant", page_icon="🎥", layout="wide", initial_sidebar_state="collapsed") 

# Fully Hide Sidebar
st.markdown(
    """
    <style>
        /* Hide the sidebar itself */
        section[data-testid="stSidebar"] {display: none !important;}
        
        /* Hide the menu button in the top-right corner */
        [data-testid="collapsedControl"] {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True
)


from pages import page_dashboard, page_entry, page_changelog, page_reports, page_reminders, page_manage_groups, page_types, page_banks, page_latest_entries, page_calculations, page_export, page_test
from utils import data  # Import the data loading function
from utils.utils import initialize_session_state

# Initialize session state for date-related values
initialize_session_state()

# ✅ Load data only once & store separately
if (
    "expenses_df" not in st.session_state
    or "incomes_df" not in st.session_state

):
    # Load all data using the function from data.py
    (
       expenses_df, incomes_df
    ) = data.load_all_data()
    
    # Store the data in session_state
    st.session_state.expenses_df = expenses_df
    st.session_state.incomes_df = incomes_df

    st.success("✅ Data loaded successfully!")


# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "page_dashboard"  # Default page

# Function to navigate
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

# Display the current page based on session state
if st.session_state.current_page == "page_dashboard":
    page_dashboard.show(navigate_to)
elif st.session_state.current_page == "page_reports":
    page_reports.show(navigate_to)
elif st.session_state.current_page == "page_reminders":
    page_reminders.show(navigate_to)
elif st.session_state.current_page == "page_entry":
    page_entry.show(navigate_to)
elif st.session_state.current_page == "page_changelog":
    page_changelog.show(navigate_to)
elif st.session_state.current_page == "page_manage_groups":
    page_manage_groups.show(navigate_to)
elif st.session_state.current_page == "page_types":
    page_types.show(navigate_to)
elif st.session_state.current_page == "page_banks":
    page_banks.show(navigate_to)
elif st.session_state.current_page == "page_latest_entries":
    page_latest_entries.show(navigate_to)
elif st.session_state.current_page == "page_calculations":
    page_calculations.show(navigate_to)
elif st.session_state.current_page == "page_export":
    page_export.show(navigate_to)
elif st.session_state.current_page == "page_test":
    page_test.show(navigate_to)

