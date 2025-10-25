import streamlit as st
import pandas as pd
from utils import data


st.title("Word Finder")
st.set_page_config(layout="wide",) 


# About
with st.expander("About", expanded=False):
    st.markdown(
        """
        🎯 The idea here is that I’d like to solve the New York Times [Wordle Game](https://www.nytimes.com/games/wordle/index.html) the easy way.
        
        📚 I've started to collect the words on the [Wikipedia main page](https://en.wikipedia.org/wiki/Main_Page) since 2024. (I update it not that frequently)
        
        🗂️ Also, there is a text file for English words in this [GitHub repository](https://github.com/dwyl/english-words/tree/master). If you select GitHub or Both in Data Source selection it can be used.
        """
    )


# Reset button
if st.button("🔄 Reset all filters"):
    # Clear filter inputs by setting session_state to empty/default
    st.session_state["word_length"] =  5
    st.session_state["starts_with"] = ""
    st.session_state["ends_with"] = ""
    st.session_state["contains"] = ""
    st.session_state["exclude_letters"] = ""
    st.session_state["position_input"] = ""
    st.session_state["unique_letters"] = False
    st.rerun()  # Refresh the app



# Data source choices
data_source_selection = st.radio("Select Data Source", ("Local", "GitHub", "Both"), horizontal=True, key="data_source_selection")


# Default selection is local
if "word_data_df" not in st.session_state:
    word_data_df = data.load_local_data()
    st.session_state.word_data_df = word_data_df
    st.session_state.word_length = 5
    max_len = int(st.session_state["word_data_df"]["word"].str.len().max())


if "word_length" not in st.session_state:
    if "word_data_df" not in st.session_state:
        max_len = 20
        
        # Word length selection
        st.session_state.word_length = 5
    else:
        # Max word length
        max_len = int(st.session_state["word_data_df"]["word"].str.len().max())
        
        # Word length selection
        st.session_state.word_length = 5


# Data Source Selection 
if data_source_selection == "Local":
    word_data_df = data.load_local_data()
    st.session_state.word_data_df = word_data_df
elif data_source_selection == "GitHub":
    github_df = data.load_github_data()
    word_data_df = github_df
    st.session_state.word_data_df = word_data_df
elif data_source_selection == "Both":
    local_df = data.load_local_data()
    github_df = data.load_github_data()
    word_data_df = pd.concat([local_df, github_df]).drop_duplicates().reset_index(drop=True)
    st.session_state.word_data_df = word_data_df
else: # Default local
    word_data_df = data.load_local_data()
    st.session_state.word_data_df = word_data_df

# After setting st.session_state.word_data_df
max_len = int(st.session_state["word_data_df"]["word"].str.len().max())



# Columns
col_filters, col_results = st.columns(2)

with col_filters:
    # Filter controls
    word_length = st.slider("Word Length", min_value=2, max_value=max_len, step=1, key="word_length")
    starts_with = st.text_input("Starts with...", key="starts_with")
    ends_with = st.text_input("Ends with...", key="ends_with")
    contains = st.text_input("Contains...", key="contains")
    exclude_letters = st.text_input("Exclude letters...", key="exclude_letters")
    position_input = st.text_input("Letter at position (e.g., 2:a,4:t)...", key="position_input")
    exclude_position_input = st.text_input("❌ Excluded letter at position (e.g., 2:a,4:t)...", key="exclude_position_input")
    unique_letters = st.checkbox("Unique Letters?", value=False, key="unique_letters")



    # Apply filters
    filtered_df = st.session_state["word_data_df"].copy()


    # Filter by word length
    filtered_df = filtered_df[filtered_df["word"].str.len() == word_length]


    # Filter by "starts with"
    if starts_with:
        filtered_df = filtered_df[filtered_df["word"].str.startswith(starts_with)]

    
    # Filter by "ends with"
    if ends_with:
        filtered_df = filtered_df[filtered_df["word"].str.endswith(ends_with)] 

    
    # Filter by "Contains" (all letters must exist anywhere)
    if contains:
        letters = list(contains)  # split input into individual letters
        filtered_df = filtered_df[
            filtered_df["word"].apply(lambda w: all(l in w for l in letters))
        ]
    

    # Filter excluding letters
    if exclude_letters:
        letters = list(exclude_letters)  # split input into individual letters
        filtered_df = filtered_df[
            filtered_df["word"].apply(lambda w: all(l not in w for l in letters))
        ]
    

    # Filter position letter pairs
    if position_input:
        # Parse input like "2:a,4:t" into a dictionary {2: 'a', 4: 't'}
        pos_dict = {}
        for item in position_input.split(","):
            if ":" in item:
                pos, letter = item.split(":")
                if pos.isdigit():
                    pos_dict[int(pos) - 1] = letter  # Convert to 0-based index

        # Apply filter
        filtered_df = filtered_df[
            filtered_df["word"].apply(lambda w: all(w[i] == l for i, l in pos_dict.items() if i < len(w)))
        ]

    # Filter excluded position letter pairs
    if exclude_position_input:
        exclude_pos_dict = {}
        for item in exclude_position_input.split(","):
            if ":" in item:
                pos, letter = item.split(":")
                if pos.isdigit():
                    exclude_pos_dict[int(pos) - 1] = letter  # 0-based index

        # Apply filter
        filtered_df = filtered_df[
            filtered_df["word"].apply(
                lambda w: all(
                    (i >= len(w)) or (w[i] != l)
                    for i, l in exclude_pos_dict.items()
                )
            )
        ]

    

    # Filter by "Unique Letters?"
    if unique_letters:
        filtered_df = filtered_df[
            filtered_df["word"].apply(lambda w: len(w) == len(set(w)))
        ]


# Second column
with col_results:
    st.write(f"Word Count: {len(filtered_df)}")

    # Sorting alphabetically beforing showing the results
    filtered_df = filtered_df.sort_values(filtered_df.columns[0])
    
    # Show results
    st.dataframe(filtered_df, hide_index=True)
