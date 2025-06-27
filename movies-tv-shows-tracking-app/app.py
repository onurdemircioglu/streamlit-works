import streamlit as st

st.set_page_config(page_title="Movies & TV Series Tracker", page_icon="🎥", layout="wide", initial_sidebar_state="collapsed") # ✅ Must be first! or error occurs: set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.

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


from pages import page_home, page_tv_shows, page_movies, page_metrics, page_latest_entries, page_data_entry, page_update, page_search, page_test
from utils import data  # Import the data loading function
from utils.utils import initialize_session_state

# Initialize session state for date-related values
initialize_session_state()

# ✅ Load data only once & store separately
if (
    "all_data_df" not in st.session_state
    or "all_movies_df" not in st.session_state
    or "all_tv_shows_df" not in st.session_state
    or "movies_watched_df" not in st.session_state
    or "tv_shows_active_df" not in st.session_state
    or "tv_shows_watched_df" not in st.session_state
    or "all_episodes_df" not in st.session_state
    or "tv_shows_last_watched_df" not in st.session_state
):
    # Load all data using the function from data.py
    (
        all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, 
        tv_shows_watched_df, tv_shows_active_df, all_episodes_df, tv_shows_last_watched_df
    ) = data.load_all_data()
    
    # Store the data in session_state
    st.session_state.all_data_df = all_data_df
    st.session_state.all_movies_df = all_movies_df
    st.session_state.all_tv_shows_df = all_tv_shows_df
    st.session_state.movies_watched_df = movies_watched_df
    st.session_state.tv_shows_watched_df = tv_shows_watched_df
    st.session_state.tv_shows_active_df = tv_shows_active_df
    st.session_state.all_episodes_df = all_episodes_df
    st.session_state.tv_shows_last_watched_df = tv_shows_last_watched_df

    st.success("✅ Data loaded successfully!")


# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "page_home"  # Default page

# Function to navigate
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

# Display the current page based on session state
if st.session_state.current_page == "page_home":
    page_home.show(navigate_to)
elif st.session_state.current_page == "page_tv_shows":
    page_tv_shows.show(navigate_to)
elif st.session_state.current_page == "page_movies":
    page_movies.show(navigate_to)
elif st.session_state.current_page == "page_metrics":
    page_metrics.show(navigate_to)
elif st.session_state.current_page == "page_latest_entries":
    page_latest_entries.show(navigate_to)
elif st.session_state.current_page == "page_data_entry":
    page_data_entry.show(navigate_to)
elif st.session_state.current_page == "page_update":
    page_update.show(navigate_to)
elif st.session_state.current_page == "page_search":
    page_search.show(navigate_to)
elif st.session_state.current_page == "page_test":
    page_test.show(navigate_to)
