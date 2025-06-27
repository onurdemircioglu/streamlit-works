import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
#import time
from utils.utils import display_menu_buttons


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters", key="add_filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            if col == "RELEASE_YEAR" or col == "DURATION":
                df[col] = df[col].astype(int)
            else:
                df[col] = df[col].dt.tz_localize(None)
                

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            

            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                if column == "RELEASE_YEAR":
                    _min = 1888
                    _max = st.session_state.current_year                    
                    step = 1
                    user_num_input = right.slider(
                        f"Values for {column}",
                        _min,
                        _max,
                        (_min, _max),
                        step=step,
                    )
                elif column == "SCORE":
                    _min = 0
                    _max = 100
                    step = 5
                    user_num_input = right.slider(
                        f"Values for {column}",
                        _min,
                        _max,
                        (_min, _max),
                        step=step,
                    )
                elif column == "DURATION":
                    _min = 0
                    _max = int(df[column].max())
                    step = int((_max - _min) / 1000)
                    user_num_input = right.slider(
                        f"Values for {column}",
                        _min,
                        _max,
                        (_min, _max),
                        step=step,
                    )
                elif column == "RATING":
                    _min = float(0)
                    _max = float(df[column].max())
                    step = 0.5
                    user_num_input = right.slider(
                        f"Values for {column}",
                        _min,
                        _max,
                        (_min, _max),
                        step=step,
                    )
                else:
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 1000
                    user_num_input = right.slider(
                        f"Values for {column}",
                        _min,
                        _max,
                        (_min, _max),
                        step=step,
                    )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df


def show(navigate_to):
    st.title("Search Page")

    display_menu_buttons(navigate_to)

    

    #df = pd.read_csv("https://raw.githubusercontent.com/mcnakhaee/palmerpenguins/master/palmerpenguins/data/penguins.csv")
    # Access stored DataFrames
    if (
        "all_data_df" in st.session_state 
        ):
        
        # Select the columns you want to keep
        selected_columns = ["ID", "TYPE", "TITLE_TYPE", "IMDB_TT", "ORIGINAL_TITLE", "PRIMARY_TITLE", "RELEASE_YEAR", "STATUS", "SCORE", "SCORE_DATE", "DURATION", "RATING", "RATING_COUNT", "GENRES", "WATCH_GRADE"]
        
        # Create a new DataFrame with only the selected columns
        #new_df = df[selected_columns].copy()
        df = st.session_state.all_data_df[selected_columns].copy()

    st.dataframe(filter_dataframe(df), hide_index=True, )
    #column_order=("ID", "TYPE", "TITLE_TYPE", "IMDB_TT", "ORIGINAL_TITLE", "PRIMARY_TITLE", "RELEASE_YEAR", "STATUS", "SCORE", "SCORE_DATE", "DURATION", "RATING", "RATING_COUNT", "GENRES", "WATCH_GRADE"), 

    st.write(
        """This app accomodates the blog [here](https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/)
        and walks you through one example of how the Streamlit
        Data Science Team builds add-on functions to Streamlit.
        """
    )

    filter_dataframe(df)
