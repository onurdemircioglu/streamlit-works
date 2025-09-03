import streamlit as st
import pandas as pd
import os

# Get the folder where the current script is (for example: utils/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Go one level up to reach the app folder (if script is in utils/)
app_dir = os.path.dirname(script_dir)

# Build path to the DB (or working file) file inside the app folder
FILE_PATH = os.path.join(app_dir, "words.txt")  # This line has been added or changed


@st.cache_data
def load_local_data():
    #return pd.read_csv(r"words.txt", header=None, names=["word"])
    #word_data_df = pd.read_csv(r"words.txt", sep="\t", header=None, names=["word"])
    word_data_df = pd.read_csv(FILE_PATH, sep="\t", header=None, names=["word"])
    return word_data_df


@st.cache_data
def load_github_data():
    github_df = pd.read_csv(
        "https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words.txt",
        sep= "\s+",   # ✅ split on whitespace
        header=None,
        names=["word"]
    )
    return github_df
