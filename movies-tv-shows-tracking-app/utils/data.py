import streamlit as st
import pandas as pd
from utils import my_functions



# Function to load all data
def load_all_data():
    obj = my_functions.MyClass()
    conn = obj.get_db_connection()
    #cursor = conn.cursor()
    
    all_data_df = pd.read_sql_query("SELECT * FROM MAIN_DATA", conn)
    all_episodes_df = pd.read_sql("SELECT * FROM EPISODES", conn)
    tv_shows_last_watched_df = pd.read_sql("SELECT * FROM TV_SHOWS_LAST_WATCHED", conn)
    

    # Create filtered DataFrames
    all_movies_df = all_data_df[all_data_df["TYPE"] == "Movie"]
    all_tv_shows_df = all_data_df[all_data_df["TYPE"] == "TV Series"]
    movies_watched_df = all_data_df[ (all_data_df["STATUS"] == "WATCHED") & (all_data_df["TYPE"] == "Movie") ]
    tv_shows_watched_df = all_data_df[ (all_data_df["STATUS"] == "WATCHED") & (all_data_df["TYPE"] == "TV Series") ]
    tv_shows_active_df = all_data_df[ (all_data_df["STATUS"] == "IN PROGRESS") & (all_data_df["TYPE"] == "TV Series") ]
    
    conn.close()
    
    return all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, tv_shows_watched_df, tv_shows_active_df, all_episodes_df, tv_shows_last_watched_df
