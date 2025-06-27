import streamlit as st
#import pandas as pd
from utils import my_functions
from utils.utils import display_menu_buttons


obj = my_functions.MyClass()


def tv_shows_actions():
    # Fetch TV Shows from Database
    #obj = my_functions.MyClass()
    tv_shows = obj.fetch_tv_shows()

    # Select a TV Show
    show_options = {f"{show_id} - {info['title']}": show_id for show_id, info in tv_shows.items()}
    selected_show_label = st.selectbox("Select a TV Show:", list(show_options.keys()))
    selected_show_id = show_options[selected_show_label]  # Extract ID from selection

    # Fetch Episode Data
    episode_numbers = obj.fetch_tv_shows_episode_numbers(selected_show_id)

    # Create two columns
    col_left, col_right = st.columns(2)

    # Left Column: Display Fetched Data
    with col_left:
        st.subheader("TV Show Details")
        if episode_numbers:
            with st.container():
                st.write("**TV Show ID:**", episode_numbers["ID"])
                st.write("**TV Show Title:**", episode_numbers["Title"])
                st.write("**Min Episode No:**", episode_numbers["Min Episode No"])
                st.write("**Max Episode No:**", episode_numbers["Max Episode No"])
                st.write("**Last Watched Episode No:**", episode_numbers["Last Watched Episode No"])
        else:
            st.warning("No data found for the selected show.")

    # Right Column: Episode Actions
    with col_right:
        
        st.subheader("Episode Actions")
        new_min_episode = st.number_input("New Min Episode No", min_value=101, value=101, step=1)
        new_max_episode = st.number_input("New Max Episode No", min_value=new_min_episode, value=new_min_episode, step=1)

        action_insert, action_mark_as_watched = st.columns(2)
        with action_insert:
            if st.button("Insert New Episodes", use_container_width=True):
                obj.insert_new_episodes(selected_show_id, new_min_episode, new_max_episode)
        
        with action_mark_as_watched:
            if st.button("Mark as Watched", use_container_width=True):
                obj.mark_episode_as_watched(selected_show_id, new_min_episode, new_max_episode)
    
    st.divider()
    st.subheader("Detail of the TV Show")

    
    # Fetch and display details
    if selected_show_id:
        show_details_df = obj.fetch_tv_shows_detail(selected_show_id)
        st.dataframe(show_details_df)  # Display in Streamlit


def show(navigate_to):
    st.title("📺 TV Shows")

    display_menu_buttons(navigate_to)


    # Access stored DataFrames
    if (
        "all_data_df" in st.session_state 
        and "tv_shows_last_watched_df" in st.session_state
    ):
        # Last 30 Days Watched
        st.write("Latest TV Shows I am following.")
        #st.image("https://via.placeholder.com/300x200", caption="Example Movie")
        tv_shows_last_watched_df2 = st.session_state.tv_shows_last_watched_df.copy()
        
        # Sorting
        tv_shows_last_watched_df2 = tv_shows_last_watched_df2.sort_values(["MAX_WATCHED_DATE", "TITLE"], ascending=[False, True]) # .reset_index(drop=True)
        
        # Printing
        st.dataframe(tv_shows_last_watched_df2.head(20), hide_index=True, column_order=("ID", "TYPE", "IMDB_TT", "TITLE", "RELEASE_YEAR", "DURATION", "RATING", "RATING_COUNT", "GENRES", "MAX_WATCHED_DATE", "LATEST_EPISODE"))

    
    st.divider()
    tv_shows_actions()







        





