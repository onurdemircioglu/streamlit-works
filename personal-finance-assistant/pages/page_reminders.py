import streamlit as st
import pandas as pd
from datetime import date
from utils.utils import display_menu_buttons
from utils import my_functions


obj = my_functions.MyClass()


# **************************************************************** REMINDER TABLE - START **************************************************************** #

def show_reminder_ui(obj):  # obj: your DB manager class
    st.header("📆 Reminder Manager")

    # --- Modes ---
    mode = st.radio("Choose Action", ["Add New Reminder", "Update Existing Reminder"], horizontal=True)

    # --- Common Fields ---
    reminder_name = st.text_input("Reminder Name")
    reminder_detail = st.text_area("Reminder Details", height=80)
    reminder_date = st.date_input("Reminder Date", value=date.today())
    reminder_category = st.selectbox("Reminder Category", ["Utility", "Loan", "Subscription", "Bill", "Other"])

    recurrence_type = st.selectbox("Recurrence Type", ["none", "weekly", "monthly", "yearly"])
    recurrence_interval = st.number_input("Recurrence Interval", min_value=1, value=1, help="Every X weeks/months etc.")

    is_active = st.checkbox("Active?", value=True)
    is_done = st.checkbox("Done?", value=False)
    done_date = st.date_input("Done Date", value=None) if is_done else None

    # --- Add New Reminder ---
    if mode == "Add New Reminder":
        if st.button("➕ Add Reminder"):
            success = obj.insert_reminder(
                reminder_date.strftime("%Y-%m-%d"),
                reminder_name,
                reminder_detail,
                reminder_category,
                recurrence_type,
                recurrence_interval,
                int(is_active),
                int(is_done),
                done_date.strftime("%Y-%m-%d") if done_date else None
            )
            if success:
                st.success("Reminder added.")
                st.rerun()
            else:
                st.error("Error adding reminder.")

    # --- Update Existing Reminder ---
    else:
        all_reminders = obj.get_all_reminders()
        reminder_dict = {f"{r['ID']} - {r['REMINDER_NAME']}": r["ID"] for r in all_reminders}
        selected = st.selectbox("Select Reminder to Update", list(reminder_dict.keys()))

        if st.button("✏️ Update Reminder"):
            reminder_id = reminder_dict[selected]
            success = obj.update_reminder(
                reminder_id,
                reminder_date.strftime("%Y-%m-%d"),
                reminder_name,
                reminder_detail,
                reminder_category,
                recurrence_type,
                recurrence_interval,
                int(is_active),
                int(is_done),
                done_date.strftime("%Y-%m-%d") if done_date else None
            )
            if success:
                st.success("Reminder updated.")
                st.rerun()
            else:
                st.error("Error updating reminder.")


def show_page_contents():

    st.title("📅 Reminder Manager")

    # Load all reminders into a DataFrame
    reminders_df = obj.get_all_reminders()

    mode = st.radio("Select Mode", ["➕ Add New", "✏️ Edit Existing"])

    # ----------- Edit Mode -----------
    if mode == "✏️ Edit Existing":
        if reminders_df.empty:
            st.warning("No reminders found.")
            st.stop()

        selected_name = st.selectbox("Select a Reminder to Edit", reminders_df["REMINDER_NAME"])
        selected_row = reminders_df[reminders_df["REMINDER_NAME"] == selected_name].iloc[0]
        reminder_id = int(selected_row["ID"])
    else:
        reminder_id = None  # New insert

    # ----------- Shared Form -----------
    with st.form("reminder_form"):
        col1, col2 = st.columns(2)

        with col1:
            reminder_date = st.date_input("Reminder Date", 
                value=selected_row["REMINDER_DATE"] if mode == "✏️ Edit Existing" else date.today()
            )

            reminder_name = st.text_input("Reminder Name", 
                value=selected_row["REMINDER_NAME"] if mode == "✏️ Edit Existing" else ""
            )

            reminder_category = st.selectbox("Category", 
                options=["Finance", "Health", "Work", "Other", "Loan", "Utility"],
                index=["Finance", "Health", "Work", "Other", "Loan", "Utility"].index(selected_row["REMINDER_CATEGORY"]) if mode == "✏️ Edit Existing" else 0
            )

            recurrence_type = st.selectbox("Recurrence Type", 
                options=["None", "Daily", "Weekly", "Monthly", "Yearly"],
                index=["None", "Daily", "Weekly", "Monthly", "Yearly"].index(selected_row["RECURRENCE_TYPE"]) if mode == "✏️ Edit Existing" else 0
            )

        with col2:
            reminder_detail = st.text_area("Reminder Detail", 
                value=selected_row["REMINDER_DETAIL"] if mode == "✏️ Edit Existing" else ""
            )

            recurrence_interval = st.number_input("Recurrence Interval", min_value=0, value=int(selected_row["RECURRENCE_INTERVAL"]) if mode == "✏️ Edit Existing" else 0)

            is_active = st.checkbox("Is Active", value=bool(selected_row["IS_ACTIVE"]) if mode == "✏️ Edit Existing" else True)
            is_done = st.checkbox("Is Done", value=bool(selected_row["IS_DONE"]) if mode == "✏️ Edit Existing" else False)

            if is_done:
                done_date = st.date_input(
                    "Done Date",
                    value=pd.to_datetime(selected_row["DONE_DATE"]).date()
                    if mode == "✏️ Edit Existing" and selected_row["DONE_DATE"]
                    else date.today()
                )
            else:
                done_date = None




        submitted = st.form_submit_button("💾 Save Reminder")

    # ----------- Save Action -----------
    if submitted:
        success = False
        if mode == "➕ Add New":
            success = obj.insert_reminder(
                str(reminder_date), reminder_name, reminder_detail, reminder_category,
                recurrence_type, int(recurrence_interval), int(is_active), int(is_done), str(done_date)
            )
        else:
            success = obj.update_reminder(
                reminder_id,
                str(reminder_date), reminder_name, reminder_detail, reminder_category,
                recurrence_type, int(recurrence_interval), int(is_active), int(is_done), str(done_date)
            )

        if success:
            st.success("✅ Reminder saved successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to save the reminder.")
    
    # Show existing reminders


    


def show_latest_reminders_by_id():
    conn = obj.get_db_connection()
    #cursor = conn.cursor()
    sql_query = "SELECT * FROM TBL_REMINDERS ORDER BY ID DESC LIMIT 10"
    latest_entries = pd.read_sql_query(sql_query, conn)
    conn.close()
    st.dataframe(latest_entries, use_container_width=True, hide_index=True)



# **************************************************************** REMINDER TABLE - END **************************************************************** #

def show(navigate_to):
    st.title("Reminders")

    display_menu_buttons(navigate_to)

    show_page_contents()

    show_latest_reminders_by_id()

