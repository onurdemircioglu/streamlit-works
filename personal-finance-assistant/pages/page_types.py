import sys
import os
import streamlit as st
import pandas as pd
import sqlite3

from utils.utils import display_menu_buttons

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import my_functions




def manage_types():
    obj = my_functions.MyClass()

    st.title("Manage Expense Types")

    types = obj.get_expense_types()
    type_dict = {name: gid for gid, name in types}

    # --- Section: Add new expense type
    with st.expander("➕ Add New Expense Type"):
        new_type = st.text_input("New Type Name")
        if st.button("Add Type"):
            if new_type.strip():
                existing = [name.lower() for name in type_dict.keys()]
                if new_type.strip().lower() in existing:
                    st.warning("This type already exists.")
                else:
                    try:
                        conn = obj.get_db_connection()
                        cur = conn.cursor()
                        cur.execute("INSERT INTO TBL_EXPENSE_TYPES_LKP (TYPE_DESC) VALUES (?)", (new_type.strip(),))
                        conn.commit()
                        conn.close()
                        st.success(f"Type '{new_type}' added.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Type name cannot be empty.")


    # --- Now check if types exist
    types = obj.get_expense_types()
    if not types:
        st.warning("No expense types found. Please add one above.")
        return



    st.subheader("✏️ Rename Expense Type")

    if types:
        name_to_edit = st.selectbox("Select type to rename", list(type_dict.keys()), key="type_rename_select")
        new_type_name = st.text_input("Enter new type name", key="type_rename_input")

        if st.button("Rename Type"):
            selected_id = type_dict[name_to_edit]
            existing_type_names = [name.lower() for name in type_dict.keys() if name != name_to_edit]

            if not new_type_name.strip():
                st.warning("New name cannot be empty.")
            elif new_type_name.strip().lower() in existing_type_names:
                st.warning("Another type with this name already exists.")
            else:
                success, error = obj.update_type_name(selected_id, new_type_name.strip())
                if success:
                    st.success("Type renamed.")
                    st.rerun()
                else:
                    st.error(f"Error: {error}")
    else:
        st.info("No types available to rename.")




    st.subheader("🗑️ Soft Delete Type")

    if types:
        type_to_delete = st.selectbox("Select type to delete", list(type_dict.keys()), key="delete_type")
        if st.button("Delete Type"):
            type_id = type_dict[type_to_delete]
            obj.soft_delete_type(type_id)
            st.success(f"Type '{type_to_delete}' deleted (soft).")
            st.rerun()
    else:
        st.info("No types to delete.")



    st.subheader("♻️ Restore Deleted Types")

    deleted_types = obj.get_deleted_types() 

    if deleted_types:
        deleted_dict = {name: gid for gid, name in deleted_types}
        selected_restore = st.selectbox("Select a type to restore", list(deleted_dict.keys()), key="restore_type")

        if st.button("Restore Type"):
            type_id = deleted_dict[selected_restore]
            obj.restore_type(type_id)
            st.success(f"Type '{selected_restore}' restored.")
            st.rerun()
    else:
        st.info("No deleted types to restore.")






def show(navigate_to):
    st.title("Types")

    display_menu_buttons(navigate_to)

    manage_types()



