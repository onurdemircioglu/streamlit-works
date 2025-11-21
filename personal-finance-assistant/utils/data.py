import streamlit as st
import pandas as pd
from utils import my_functions

obj = my_functions.MyClass()

# Function to load all data
def load_all_data():
    conn = obj.get_db_connection()
    #cursor = conn.cursor()
    
    #expenses_df = pd.read_sql_query("SELECT * FROM TBL_EXPENSES", conn)
    reportable_expenses_df = pd.read_sql_query("SELECT * FROM REPORTABLE_EXPENSES", conn)
    incomes_df = pd.read_sql("SELECT * FROM TBL_INCOMES", conn)
    
    conn.close()
    
    return reportable_expenses_df, incomes_df