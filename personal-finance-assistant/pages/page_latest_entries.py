import streamlit as st
import pandas as pd
from utils.utils import display_menu_buttons
from utils import my_functions

obj = my_functions.MyClass()

def show_latest_entries():
    conn = obj.get_db_connection()
    #cursor = conn.cursor()
    sql_query = """
                SELECT A.ID, EXPENSE_DATE, B.EXPENSE_GROUP, C.EXPENSE_SUBGROUP, EXPENSE_PLACE, EXPENSE_DETAIL, EXPENSE_AMOUNT,
                INSTALLMENT_STATUS, INSTALLMENT_COUNT, NO_OF_INSTALLMENT, D.BANK_NAME, D.DETAIL_NAME, EXPENSE_NOTE
                FROM TBL_EXPENSES A 
                
                LEFT JOIN TBL_EXPENSE_GROUPS_LKP B
                ON A.EXPENSE_GROUP = B.ID

                LEFT JOIN TBL_EXPENSE_SUBGROUPS_LKP C
                ON A.EXPENSE_SUBGROUP = C.ID

                LEFT JOIN TBL_BANKS_LKP D
                ON A.BANK_ID = D.ID

                ORDER BY A.ID DESC LIMIT 30
                """
    last_entries = pd.read_sql_query(sql_query, conn)
    conn.close()

    st.dataframe(last_entries, hide_index=True)
    #st.rerun()


def show(navigate_to):
    st.title("Latest Entries")

    display_menu_buttons(navigate_to)

    show_latest_entries()



