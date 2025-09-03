import streamlit as st
import pandas as pd


@st.cache_data
def load_local_data():
    #return pd.read_csv(r"words.txt", header=None, names=["word"])
    word_data_df = pd.read_csv(r"words.txt", sep="\t", header=None, names=["word"])
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
