import streamlit as st
from utils.utils import display_menu_buttons

def show(navigate_to):
    st.title("Test Page")

    display_menu_buttons(navigate_to)

    st.write("This is a test page")