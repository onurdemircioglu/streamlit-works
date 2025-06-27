import sys
import os
import streamlit as st
import pandas as pd
import sqlite3

from utils.utils import display_menu_buttons

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import my_functions




def manage_banks():
    obj = my_functions.MyClass()

    st.title("Manage Banks")

    banks = obj.get_banks()
    #banks_dict = {name: gid for gid, name in banks}
    banks_dict = {bank_name: bank_id for bank_id, bank_name, _, _ in banks}
    #banks_dict = {f"{bank_name} - {detail_name}": bank_id for bank_id, bank_name, detail_name, _ in banks}


    # --- Section: Add new bank
    with st.expander("➕ Add New Bank Detail"):
        new_bank = st.text_input("New Bank Name")
        #bank_name = st.text_input("Bank Name")
        detail_name = st.text_input("Account / Card etc. Detail")

        # Let user associate an expense type
        types = obj.get_expense_types()
        type_dict = {name: gid for gid, name in types}
        available_types = [name for name in type_dict.keys()]

        #available_types = ["Account", "Card", "Cash", "ABC", "Other"]  # or fetch from DB if dynamic
        bank_type = st.selectbox("Associated Expense Type", options=available_types)

        if st.button("Add Bank Detail"):
            if not (new_bank.strip() and detail_name.strip() and bank_type.strip()):
                st.warning("Please fill all fields.")
            else:
                existing = [name.lower() for name in banks_dict.keys()]
                if new_bank.strip().lower() in existing:
                    st.warning("This bank already exists.")
                else:
                    try:
                        conn = obj.get_db_connection()
                        cur = conn.cursor()
                        cur.execute("""
                            INSERT INTO TBL_BANKS_LKP (BANK_NAME, DETAIL_NAME, BANK_TYPE)
                            VALUES (?, ?, ?)
                        """, (new_bank.strip(), detail_name.strip(), bank_type.strip()))
                        conn.commit()
                        conn.close()
                        st.success("Bank detail added successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")


    # --- Now check if bank exist
    banks = obj.get_banks()
    if not banks:
        st.warning("No bank name found. Please add one above.")
        return


    """st.subheader("✏️ Rename Bank")

    if banks:
        name_to_edit = st.selectbox("Select bank to edit", list(banks_dict.keys()), key="bank_rename_select")
        selected_id = banks_dict[name_to_edit]

        # Fetch current details for selected bank
        current_details = obj.get_bank_detail_by_id(selected_id)
        current_detail_name = current_details.get("DETAIL_NAME", "")
        current_bank_type = current_details.get("BANK_TYPE", "")

        # Editable fields
        new_bank_name = st.text_input("Bank Name", value=name_to_edit, key="bank_name_input")
        new_detail_name = st.text_input("Account / Card Detail (do not enter sensitive or confidential information)", value=current_detail_name, key="detail_name_input")

        # Let user associate an expense type
        types = obj.get_expense_types()
        type_dict = {name: gid for gid, name in types}
        available_types = [name for name in type_dict.keys()]

        new_bank_type = st.selectbox("Associated Expense Type", available_types, 
                                    index=available_types.index(current_bank_type) if current_bank_type in available_types else 0,
                                    key="bank_type_input")

        if st.button("Update Bank"):
            existing_bank_names = [name.lower() for name in banks_dict.keys() if name != name_to_edit]

            if not new_bank_name.strip():
                st.warning("Bank name cannot be empty.")
            elif new_bank_name.strip().lower() in existing_bank_names:
                st.warning("Another bank with this name already exists.")
            else:
                success, error = obj.update_bank_full(selected_id, new_bank_name.strip(), new_detail_name.strip(), new_bank_type)
                if success:
                    st.success("Bank information updated.")
                    st.rerun()
                else:
                    st.error(f"Error: {error}")


    else:
        st.info("No banks available to edit.")"""




    st.subheader("✏️ Rename Bank")

    if banks:
        name_to_edit = st.selectbox("Select bank to edit", list(banks_dict.keys()), key="bank_rename_select")
        selected_id = banks_dict[name_to_edit]

        # Fetch current details for selected bank
        current_details = obj.get_bank_detail_by_id(selected_id)
        current_detail_name = current_details.get("DETAIL_NAME", "")
        current_bank_type = current_details.get("BANK_TYPE", "")

        # Editable fields
        new_bank_name = st.text_input("Bank Name", value=name_to_edit, key="bank_name_input")
        new_detail_name = st.text_input("Account / Card Detail (do not enter sensitive or confidential information)", value=current_detail_name, key="detail_name_input")

        # Let user associate an expense type
        types = obj.get_expense_types()
        type_dict = {name: gid for gid, name in types}
        available_types = list(type_dict.keys())

        new_bank_type = st.selectbox(
            "Associated Expense Type",
            available_types,
            index=available_types.index(current_bank_type) if current_bank_type in available_types else 0,
            key="bank_type_input"
        )

        if st.button("Update Bank"):
            new_bank_name_clean = new_bank_name.strip().lower()
            new_detail_name_clean = new_detail_name.strip().lower()

            # Get all banks (ID, BANK_NAME, DETAIL_NAME, BANK_TYPE)
            all_banks = obj.get_banks()  # Expects list of tuples: (id, name, detail, type)

            # Build (name, detail) set, excluding the current one being edited
            existing_combos = {
                (name.strip().lower(), detail.strip().lower())
                for bank_id, name, detail, _ in all_banks
                if bank_id != selected_id
            }

            if not new_bank_name.strip():
                st.warning("Bank name cannot be empty.")
            elif not new_detail_name.strip():
                st.warning("Detail name cannot be empty.")
            elif (new_bank_name_clean, new_detail_name_clean) in existing_combos:
                st.warning("Another bank with the same name and detail already exists.")
            else:
                success, error = obj.update_bank_full(selected_id, new_bank_name.strip(), new_detail_name.strip(), new_bank_type)
                if success:
                    st.success("Bank information updated.")
                    st.rerun()
                else:
                    st.error(f"Error: {error}")

    else:
        st.info("No banks available to edit.")












    st.subheader("🗑️ Soft Delete Bank")

    if banks:
        bank_to_delete = st.selectbox("Select bank to delete", list(banks_dict.keys()), key="delete_bank")
        if st.button("Delete Bank"):
            bank_id = banks_dict[bank_to_delete]
            obj.soft_delete_bank(bank_id)
            st.success(f"Bank '{bank_to_delete}' deleted (soft).")
            st.rerun()
    else:
        st.info("No banks to delete.")



    st.subheader("♻️ Restore Deleted Banks")

    deleted_banks = obj.get_deleted_banks() 

    if deleted_banks:
        deleted_dict = {name: gid for gid, name in deleted_banks}
        selected_restore = st.selectbox("Select a bank to restore", list(deleted_dict.keys()), key="restore_bank")

        if st.button("Restore Bank"):
            bank_id = deleted_dict[selected_restore]
            obj.restore_bank(bank_id)
            st.success(f"Bank '{selected_restore}' restored.")
            st.rerun()
    else:
        st.info("No deleted banks to restore.")






def show(navigate_to):
    st.title("Banks")

    display_menu_buttons(navigate_to)

    manage_banks()





