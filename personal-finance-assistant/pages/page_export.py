import streamlit as st
import pandas as pd
#from datetime import date
from utils.utils import display_menu_buttons
from utils import my_functions


obj = my_functions.MyClass()

    
def show(navigate_to):

    st.title("📤 Export")

    display_menu_buttons(navigate_to)

    # Step 1: Fetch available tables/views
    objects = obj.list_all_db_objects()
    #print(objects)

    if not objects:
        st.warning("No tables or views found.")
    else:
        object_options = [f"{obj['type'].capitalize()}: {obj['name']}" for obj in objects]
        selected = st.selectbox("Select a table or view to export", object_options)

        # Step 2: Parse selected object name
        selected_name = selected.split(": ")[1]

        # Step 3: Preview data
        conn = obj.get_db_connection()
        df = pd.read_sql_query(f"SELECT * FROM {selected_name}", conn)
        conn.close()

        st.write("### Preview (first 100 rows)")
        st.dataframe(df.head(100), hide_index=True)

        # Step 4: Export as CSV
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Export as CSV",
            data=csv,
            file_name=f"{selected_name}.csv",
            mime="text/csv"
        )