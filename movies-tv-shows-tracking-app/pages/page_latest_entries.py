import streamlit as st
#import sqlite3
import pandas as pd
from utils import my_functions
from utils.utils import display_menu_buttons

obj = my_functions.MyClass()


def show(navigate_to):
    st.title("Last 10 Entries")

    display_menu_buttons(navigate_to)



    conn = obj.get_db_connection()
    #cursor = conn.cursor()
    sql_query = "SELECT * FROM MAIN_DATA ORDER BY ID DESC LIMIT 10"
    last_entries = pd.read_sql_query(sql_query, conn)
    conn.close()

    st.dataframe(last_entries, hide_index=True)
    st.rerun()