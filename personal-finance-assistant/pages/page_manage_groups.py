import sys
import os
import streamlit as st
import pandas as pd
import sqlite3
import time

from utils.utils import display_menu_buttons

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import my_functions




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
    selected_group_name = st.selectbox("Select Expense Group", options=list(group_dict.keys()))
    selected_group_id = group_dict.get(selected_group_name)

    if selected_group_id is None:
        st.warning("Selected group not found.")
        st.stop()



    st.subheader("✏️ Rename Expense Group")

    if groups:
        name_to_edit = st.selectbox("Select group to rename", list(group_dict.keys()), key="group_rename_select")
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
        subgroup_to_edit = st.selectbox("Select Subgroup to Rename", list(name_id_map.keys()))
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
        group_to_delete = st.selectbox("Select group to delete", list(group_dict.keys()), key="delete_group")
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
        selected_restore = st.selectbox("Select a group to restore", list(deleted_dict.keys()), key="restore_group")

        if st.button("Restore Group"):
            group_id = deleted_dict[selected_restore]
            obj.restore_group(group_id)
            st.success(f"Group '{selected_restore}' restored.")
            time.sleep(1) # Screen doesn't show the st.success info because it is too fast.
            st.rerun()
    else:
        st.info("No deleted groups to restore.")






def show(navigate_to):
    st.title("Groups")

    display_menu_buttons(navigate_to)

    manage_group_subgroups()



