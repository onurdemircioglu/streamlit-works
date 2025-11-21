import sys
import os
import streamlit as st
import pandas as pd
#from datetime import date
import sqlite3
import time
from utils.utils import display_menu_buttons
from utils import my_functions
from utils.streamlit_helpers import smart_selectbox, smart_text_input, smart_text_area, smart_number_input, smart_date_input

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


obj = my_functions.MyClass()


def show(navigate_to):
    #st.title("⚙️ Settings")
    st.title("🛠️ Settings")

    display_menu_buttons(navigate_to)

    tabs = st.tabs(["Manage Groups", "Manage Types", "Manage Banks", "💰 Manage Incomes"])


    with tabs[0]:
        manage_group_subgroups()
    
    with tabs[1]:
        manage_types()
    
    with tabs[2]:
        manage_banks()
    
    with tabs[3]:
        manage_incomes()



# **************************************************************** MANAGE GROUPS - START **************************************************************** #

def manage_group_subgroups():
    obj = my_functions.MyClass()

    st.title("Manage Expense Subgroups")

    groups = obj.get_expense_groups()
    group_dict = {name: gid for gid, name in groups}

    # --- Section: Add new expense group
    with st.expander("➕ Add New Expense Group"):
        new_group = st.text_input("New Group Name")
        if st.button("Add Group"):
            if new_group.strip():
                existing = [name.lower() for name in group_dict.keys()]
                if new_group.strip().lower() in existing:
                    st.warning("This group already exists.")
                else:
                    try:
                        conn = obj.get_db_connection()
                        cur = conn.cursor()
                        cur.execute("INSERT INTO TBL_EXPENSE_GROUPS_LKP (EXPENSE_GROUP) VALUES (?)", (new_group.strip(),))
                        conn.commit()
                        conn.close()
                        st.success(f"Group '{new_group}' added.")
                        time.sleep(1) # Screen doesn't show the st.success info because it is too fast.
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Group name cannot be empty.")


    # --- Now check if groups exist
    groups = obj.get_expense_groups()
    if not groups:
        st.warning("No expense groups found. Please add one above.")
        return

    group_dict = {name: gid for gid, name in groups}
    #selected_group_name = st.selectbox("Select Expense Group", options=list(group_dict.keys()))
    selected_group_name = smart_selectbox(label="Select Expense Group", options=list(group_dict.keys()), key="key_selected_group_name")
    selected_group_id = group_dict.get(selected_group_name)

    if selected_group_id is None:
        st.warning("Selected group not found.")
        st.stop()



    st.subheader("✏️ Rename Expense Group")

    if groups:
        #name_to_edit = st.selectbox("Select group to rename", list(group_dict.keys()), key="group_rename_select")
        name_to_edit = smart_selectbox(label="Select group to rename", options=list(group_dict.keys()), key="group_rename_select")
        new_group_name = st.text_input("Enter new group name", key="group_rename_input")

        if st.button("Rename Group"):
            selected_id = group_dict[name_to_edit]
            existing_group_names = [name.lower() for name in group_dict.keys() if name != name_to_edit]

            if not new_group_name.strip():
                st.warning("New name cannot be empty.")
            elif new_group_name.strip().lower() in existing_group_names:
                st.warning("Another group with this name already exists.")
            else:
                success, error = obj.update_group_name(selected_id, new_group_name.strip())
                if success:
                    st.success("Group renamed.")
                    time.sleep(1) # Screen doesn't show the st.success info because it is too fast.
                    st.rerun()
                else:
                    st.error(f"Error: {error}")
    else:
        st.info("No groups available to rename.")




    st.markdown(f"### Subgroups under: **{selected_group_name}**")

    subgroups = obj.get_subgroups_by_group_id(selected_group_id)
    df = pd.DataFrame(subgroups, columns=["ID", "Subgroup Name"])
    st.dataframe(df, use_container_width=True)

    
    # --- Add new subgroup
    st.subheader("Add New Subgroup")
    new_subgroup = st.text_input("New Subgroup Name")
    if st.button("Add Subgroup"):
        if new_subgroup.strip():
            # Normalize comparison (case-insensitive)
            existing_subgroups = [name.lower() for _, name in subgroups]
            if new_subgroup.strip().lower() in existing_subgroups:
                st.warning("This subgroup already exists under the selected group.")
            else:
                obj.insert_subgroup(selected_group_id, new_subgroup.strip())
                st.success("Subgroup added.")
                time.sleep(1) # Screen doesn't show the st.success info because it is too fast.
                st.rerun()
        else:
            st.warning("Subgroup name cannot be empty.")


    # --- Rename existing subgroup
    st.subheader("Rename Subgroup")
    if subgroups:
        name_id_map = {name: sid for sid, name in subgroups}
        #subgroup_to_edit = st.selectbox("Select Subgroup to Rename", list(name_id_map.keys()))
        subgroup_to_edit = smart_selectbox(label="Select Subgroup to Rename", options=list(name_id_map.keys()), key="key_subgroup_to_edit")
        new_name_input = st.text_input("New Name", key="rename_input")

        if st.button("Rename Subgroup"):
            sid = name_id_map[subgroup_to_edit]
            new_name_clean = new_name_input.strip().lower()

            # Check for duplicate name under this group (excluding the one being edited)
            existing_names = {name.lower(): id_ for id_, name in subgroups if id_ != sid}

            if not new_name_clean:
                st.warning("New name cannot be empty.")
            elif new_name_clean in existing_names:
                st.warning(f"Subgroup '{new_name_input}' already exists under the selected group.")
            else:
                """obj.update_subgroup(sid, new_name_input.strip())
                st.success("Subgroup renamed.")
                st.rerun()"""


                try:
                    obj.update_subgroup(sid, new_name_input.strip())
                    st.success("Subgroup renamed.")
                    time.sleep(1) # Screen doesn't show the st.success info because it is too fast.
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Rename failed: subgroup with this name already exists.")


    else:
        st.info("No subgroups to rename.")




    st.subheader("🗑️ Soft Delete Group")

    if groups:
        #group_to_delete = st.selectbox("Select group to delete", list(group_dict.keys()), key="delete_group")
        group_to_delete = smart_selectbox(label="Select group to delete", options=list(group_dict.keys()), key="delete_group")
        if st.button("Delete Group"):
            group_id = group_dict[group_to_delete]
            obj.soft_delete_group(group_id)
            st.success(f"Group '{group_to_delete}' deleted (soft).")
            time.sleep(1) # Screen doesn't show the st.success info because it is too fast.
            st.rerun()
    else:
        st.info("No groups to delete.")




    st.subheader("♻️ Restore Deleted Groups")

    deleted_groups = obj.get_deleted_groups() 

    if deleted_groups:
        deleted_dict = {name: gid for gid, name in deleted_groups}
        #selected_restore = st.selectbox("Select a group to restore", list(deleted_dict.keys()), key="restore_group")
        selected_restore = smart_selectbox(label="Select a group to restore", options=list(deleted_dict.keys()), key="restore_group")

        if st.button("Restore Group"):
            group_id = deleted_dict[selected_restore]
            obj.restore_group(group_id)
            st.success(f"Group '{selected_restore}' restored.")
            time.sleep(1) # Screen doesn't show the st.success info because it is too fast.
            st.rerun()
    else:
        st.info("No deleted groups to restore.")



# **************************************************************** MANAGE GROUPS - END **************************************************************** #



# **************************************************************** MANAGE TYPES - START **************************************************************** #


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

        
# **************************************************************** MANAGE TYPES - END **************************************************************** #


# **************************************************************** MANAGE BANKS - START **************************************************************** #


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



    st.subheader("✏️ Rename Bank")

    if banks:
        name_to_edit = st.selectbox("Select bank to edit", list(banks_dict.keys()), key="bank_rename_select")
        selected_id = banks_dict[name_to_edit]

        # Fetch current details for selected bank
        current_details = obj.get_bank_detail_by_id(selected_id)
        current_detail_name = current_details.get("DETAIL_NAME", "")
        current_bank_type = current_details.get("BANK_TYPE", "")

        # Editable fields
        #new_bank_name = st.text_input("Bank Name", value=name_to_edit, key="bank_name_input")
        new_bank_name = smart_text_input(label="Bank Name", default=name_to_edit if name_to_edit else "", key="bank_name_input")
        #new_detail_name = st.text_input("Account / Card Detail (do not enter sensitive or confidential information)", value=current_detail_name, key="detail_name_input")
        new_detail_name = smart_text_input(
            label="Account / Card Detail (do not enter sensitive or confidential information)",
            default=current_detail_name if current_detail_name else "",
            key="detail_name_input"
            )

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



# **************************************************************** MANAGE BANKS - END **************************************************************** #



# **************************************************************** INCOMES - START **************************************************************** #

def manage_incomes():
    st.title("💰 Income Management")

    tab_insert, tab_update_delete, tab_income_types = st.tabs(["➕ Add Income", "✏️ Update / Delete Income", "⚙ Manage Income Types"])

# **************************************************************** INSERT INCOME - START **************************************************************** #
    with tab_insert:
        st.subheader("Add New Income")
        
        types_df = obj.get_income_types()
        if types_df.empty:
            st.warning("⚠ No income types found.")
            with st.expander("➕ Add New Income Type"):
                new_type_name = st.text_input("New Income Type Name")
                if st.button("Save Type"):
                    if new_type_name.strip():
                        obj.insert_income_type(new_type_name.strip())
                        st.success(f"✅ '{new_type_name}' added successfully!")
                        st.rerun()  # Refresh the page to load new types
                    else:
                        st.error("Type name cannot be empty.")
            st.stop()  # Stop further UI rendering until types exist
            #st.warning("⚠ No income types found. Please add income types first in the Settings page.")



        col_insert_income_1, col_insert_income_2 = st.columns(2)

        with col_insert_income_1:
            #income_date = st.date_input("Income Date", value=st.session_state.current_day)
            income_date = smart_date_input("Income Date", default=st.session_state.current_day, key="key_income_date")
            #income_amount = st.number_input("Income Amount", min_value=0.0, step=100.0)
            income_amount = smart_number_input(label="Income Amount", min_value=0.0, step=100.0, key="key_income_amount")
            income_source = st.text_input("Income Source")
        
        with col_insert_income_2:
            income_type = st.selectbox("Income Type", types_df["TYPE_NAME"])
            income_type_id = types_df.loc[types_df["TYPE_NAME"] == income_type, "ID"].values[0]
            note = st.text_area("Note")

        # Action buttons
        if st.button("💾 Save"):
            if income_amount > 0:
                obj.insert_income(
                    income_date.strftime("%Y-%m-%d"),
                    int(income_type_id),
                    income_amount,
                    income_source,
                    note
                )
                st.success("✅ Income saved successfully!")
            else:
                st.error("Income amount must be greater than 0.")

        
        obj.draw_separator(color="#01055b", thickness=1, radius=12)
        
        
        incomes_df = obj.get_all_incomes()
        st.dataframe(incomes_df, hide_index=True)


# **************************************************************** INSERT INCOME - END **************************************************************** #

    
# **************************************************************** UPDATE / DELETE INCOME - START **************************************************************** #
    with tab_update_delete:
        st.subheader("Update or Delete Incomes")
        
        incomes_df = obj.get_all_incomes()

        obj.draw_separator(color="#01055b", thickness=1, radius=12)
        
        if not incomes_df.empty:
            st.dataframe(incomes_df, hide_index=True)
            selected_id = st.selectbox("Select an Income by ID", incomes_df["ID"])
            selected_row = incomes_df[incomes_df["ID"] == selected_id].iloc[0]

            upd_col_1, upd_col_2 = st.columns(2)

            
            
            with upd_col_1:
                #upd_date = st.date_input("Income Date", pd.to_datetime(selected_row["INCOME_DATE"]).date(), key="upd_income_date")
                upd_date = smart_date_input(label="Income Date", default=pd.to_datetime(selected_row["INCOME_DATE"]).date(), key="upd_income_date")
                #upd_amount = st.number_input("Income Amount", value=float(selected_row["INCOME_AMOUNT"]), key="upd_income_amount")
                upd_amount = smart_number_input(label="Income Amount", default=float(selected_row["INCOME_AMOUNT"]), key="upd_income_amount")
                upd_is_active = st.selectbox("Is Active?",options={0,1}, index=1, key="upd_income_is_active")


            with upd_col_2:
                try:
                    default_index = int(types_df[types_df["TYPE_NAME"] == selected_row["INCOME_TYPE"]].index[0])
                except IndexError:
                    default_index = 0  # fallback to first option
                
                upd_type = st.selectbox("Income Type", types_df["TYPE_NAME"], index=default_index, key="upd_income_type")
                upd_type_id = types_df.loc[types_df["TYPE_NAME"] == upd_type, "ID"].values[0]
                #upd_source = st.text_input("Income Source", value=selected_row["INCOME_SOURCE"] or "", key="upd_income_source")
                upd_source = smart_text_input(label="Income Source", default=selected_row["INCOME_SOURCE"] or "", key="upd_income_source")
                #upd_note = st.text_area("Note", value=selected_row["NOTE"] or "", key="upd_note")
                upd_note = smart_text_area(label="Note", default=selected_row["NOTE"] or "", key="upd_note")
            

            upd_income_save_col, upd_income_delete_col = st.columns(2)

            with upd_income_save_col:
                if st.button("💾 Update"):
                    if obj.update_income(selected_id, str(upd_date), int(upd_type_id), upd_amount, upd_source, upd_note, upd_is_active):
                        st.success("Income updated successfully!")
                        time.sleep(1)
                        st.rerun() # To show the updated incomes in incomes_df

            
            with upd_income_delete_col:
                if st.button("🗑️ Delete", key="key_soft_delete_income"):
                    if obj.soft_delete_income(selected_id):
                        st.warning("Income deleted.")
                        time.sleep(1)
                        st.rerun() # To show the updated incomes in incomes_df
            
            
        else:
            st.info("No income records found.")

# **************************************************************** UPDATE / DELETE INCOME - END **************************************************************** #


# **************************************************************** INSERT / UPDATE / DELETE INCOME TYPES - START **************************************************************** #
    with tab_income_types:
        st.subheader("Insert / Update / Delete Income Types")

        income_types_df = obj.get_income_types()
        income_type_dict = dict(zip(income_types_df["TYPE_NAME"], income_types_df["ID"])) # income_type_dict = {name: gid for gid, name, _ in income_types_df} The _ ignores the third column (IS_ACTIVE).

        st.dataframe(income_types_df, hide_index=True)

        obj.draw_separator(color="#01055b", thickness=1, radius=12)

        # ✅ ADD NEW TYPE
        with st.expander("➕ Add New Income Type"):
            new_type = st.text_input("New Income Type")
            if st.button("Save New Type"):
                existing_income_type_names = [name.lower() for name in income_type_dict.keys()]
                if new_type.strip().lower() in existing_income_type_names:
                    st.error("This income type already exists.")
                elif new_type.strip():
                    obj.insert_income_type(new_type.strip())
                    st.success(f"✅ '{new_type}' added successfully!")
                    st.rerun()
                else:
                    st.error("Type name cannot be empty.")

        
        obj.draw_separator(color="#01055b", thickness=1, radius=12)
        

        
        # Rename / Delete / Restore Income Type
        if not income_types_df.empty:
            col_income_name_to_edit, col_income_change_actions = st.columns(2)

            with col_income_name_to_edit:
                income_name_to_edit = st.selectbox("Select income type to rename", list(income_type_dict.keys()), key="income_type_rename_select") # Key is the name of income type. Since there is a uniqueness control it shouldn't be a problem.
                renamed_income_type = smart_text_input("Enter new income type name", key="key_renamed_income_type")
            
            with col_income_change_actions:
                if st.button("💾 Rename"):
                    selected_id = income_type_dict[income_name_to_edit]

                    obj.update_income_type(selected_id, renamed_income_type)
                    st.success(f"Updated: from {income_name_to_edit} to {renamed_income_type}")
                    time.sleep(1)
                    #st.session_state["key_renamed_income_type"] = "" # TODO: Clearing the widget value after update. There is a problem here that I couldn't fix yet.
                    st.rerun()
                
                if st.button("🗑️ Delete", key="key_soft_delete_income_type"):
                    selected_id = income_type_dict[income_name_to_edit]

                    obj.soft_delete_income_type(selected_id)
                    st.success(f"Income type (soft) deleted: {income_name_to_edit}")
                    time.sleep(1)
                    #st.session_state["key_renamed_income_type"] = "" # TODO: Clearing the widget value after update. There is a problem here that I couldn't fix yet.
                    st.rerun()
                
                if st.button("♻ Restore"):
                    selected_id = income_type_dict[income_name_to_edit]                    
                    is_active = income_types_df.loc[income_types_df["TYPE_NAME"] == income_name_to_edit, "IS_ACTIVE"].iloc[0]
                    
                    if is_active == 1:
                        st.warning("Income Type is already active")
                        time.sleep(1)
                    else:
                        obj.restore_income_type(selected_id)
                        st.success(f"Income type restored: {income_name_to_edit}")
                        time.sleep(1)
                        st.rerun()


# **************************************************************** INSERT / UPDATE / DELETE INCOME TYPES - END **************************************************************** #


