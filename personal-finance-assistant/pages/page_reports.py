
# Hiç başlanmadıIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

import streamlit as st
from utils.utils import display_menu_buttons


def show(navigate_to):
    st.title("Expense Entry")

    display_menu_buttons(navigate_to)

    st.header("Work in Progress")