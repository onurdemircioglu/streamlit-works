import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.utils import display_menu_buttons


def show(navigate_to):
    st.title("Metrics")
    #st.subheader("Metrics")

    display_menu_buttons(navigate_to)



    # Access current_year from session_state
    #current_year = st.session_state.current_year
    #current_year = st.session_state.get('current_year', 'Not Set')
    #current_month = st.session_state.get('current_month', 'Not Set')

    # Now you can use current_year in calculations or display
    #st.write(f"Current Year: {current_year}")
    #st.write(f"Current Month: {current_month}")


    # Access stored DataFrames
    if (
        "all_data_df" in st.session_state 
        and "all_movies_df" in st.session_state 
        and "movies_watched_df" in st.session_state
        and "all_tv_shows_df" in st.session_state
        and "tv_shows_watched_df" in st.session_state
        and "tv_shows_active_df" in st.session_state
        and "all_episodes_df" in st.session_state
    ):
        # Metrics
        total_records_count = len(st.session_state.all_data_df)
        movies_count = len(st.session_state.all_movies_df)
        tv_shows_count = len(st.session_state.all_tv_shows_df)
        unknown_type_count = total_records_count - (movies_count + tv_shows_count)
        movies_watched_count = len(st.session_state.movies_watched_df)
        movies_watched_this_year_count = len(st.session_state.movies_watched_df[ st.session_state.movies_watched_df["SCORE_DATE"].str.startswith(str(st.session_state.current_year)) ])
        
        movies_watched_this_month_count = len(
            st.session_state.movies_watched_df[
                st.session_state.movies_watched_df["SCORE_DATE"].str.startswith(
                    f"{st.session_state.current_year}-{str(st.session_state.current_month).zfill(2)}"
                )
            ]
        )

        tv_shows_watched_count = len(st.session_state.tv_shows_watched_df)
        tv_show_active_count = len(st.session_state.tv_shows_active_df)
        tv_show_watched_episode_this_year_count = len(st.session_state.all_episodes_df[ st.session_state.all_episodes_df["WATCHED_DATE"].str.startswith(str(st.session_state.current_year)) ]) 
        tv_show_watched_episode_this_month_count = len(
            st.session_state.all_episodes_df[
                st.session_state.all_episodes_df["WATCHED_DATE"].str.startswith(
                    f"{st.session_state.current_year}-{str(st.session_state.current_month).zfill(2)}"
                )
            ]
        )
        


        with st.container():
            col1, col2, col3, col4 = st.columns(4)

        with col1:
            #st.metric(label = "All Time Watched Movies", value = watched_movies_count)
            st.metric(label = "Record Count", value = total_records_count)
            
        with col2:
            st.metric(label = "Movies", value = movies_count)
            st.metric(label = "Watched All Times", value = movies_watched_count)
            st.metric(label = "Watched This Year", value = movies_watched_this_year_count)
            st.metric(label = "Watched This Month", value = movies_watched_this_month_count)
            
        with col3:
            st.metric(label = "TV Shows", value = tv_shows_count)
            st.metric(label = "Watched All Times", value = tv_shows_watched_count)
            st.metric(label = "Active Count", value = tv_show_active_count)
            st.metric(label = "Episodes Watched This Year", value = tv_show_watched_episode_this_year_count)
            st.metric(label = "Episodes Watched This Month", value = tv_show_watched_episode_this_month_count)
            
        with col4:
            st.metric(label = "Unkown Type Count", value = unknown_type_count)


        # ************************************************ #
        # ************************************************ #
        # ************************************************ #
        
        # Creating graphic of watched movies by year
        year_graph_df = st.session_state.movies_watched_df.copy()

        # Extract year from SCORE_DATE (assuming format is "YYYY-MM-DD")
        year_graph_df["Year"] = year_graph_df["SCORE_DATE"].str[:4]

        # Filter out invalid years (before 2000)
        year_graph_df = year_graph_df[year_graph_df["Year"].astype(int) >= 2000]

        # Count movies per year
        movies_per_year = year_graph_df["Year"].value_counts().reset_index()
        movies_per_year.columns = ["Year", "Count"]
        movies_per_year = movies_per_year.sort_values("Year")

        # Plot the bar chart
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(movies_per_year["Year"], movies_per_year["Count"], color="royalblue")

        # Add labels and title
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Movies Watched")
        ax.set_title("Movies Watched Per Year")
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Add data points on top of the bars
        for bar in bars:
            yval = bar.get_height()  # height of the bar
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, str(int(yval)), 
                    ha='center', va='bottom', fontweight='bold')

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Display in Streamlit
        st.pyplot(fig)

    else:
        st.warning("No data available. Please load data first.")
