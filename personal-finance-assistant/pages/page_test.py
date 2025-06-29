import streamlit as st
from utils.utils import display_menu_buttons
from utils import my_functions
import sqlite3

obj = my_functions.MyClass()

def show(navigate_to):
    st.title("Test Page")

    display_menu_buttons(navigate_to)

    st.write("I am Test Page, leave this page immediately")


    conn = sqlite3.connect(r"C:\Users\Onurdemir\Documents\Projects\personal_finance_assistant\database\budget_management.db")
    conn.execute("PRAGMA journal_mode=WAL;")
