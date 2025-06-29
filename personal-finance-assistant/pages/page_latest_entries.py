import streamlit as st
import pandas as pd
from utils.utils import display_menu_buttons
from utils import my_functions

obj = my_functions.MyClass()

# TODO: Bu fonksiyonunun my_function.py altına tranfser edilmesi
def show_latest_entries():
    conn = obj.get_db_connection()
    #cursor = conn.cursor()
    sql_query = "SELECT * FROM REPORTABLE_EXPENSES ORDER BY ID DESC LIMIT 30"
    last_entries = pd.read_sql_query(sql_query, conn)
    conn.close()

    st.dataframe(last_entries, hide_index=True)
    #st.rerun()


def show(navigate_to):
    st.title("Latest Entries")

    display_menu_buttons(navigate_to)

    show_latest_entries()



