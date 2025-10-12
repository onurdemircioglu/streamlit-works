import streamlit as st
from utils.utils import display_menu_buttons
from utils import my_functions

obj = my_functions.MyClass()

def show(navigate_to):
    st.title("Test Page")

    display_menu_buttons(navigate_to)

    st.write("I am Test Page, leave this page immediately")
