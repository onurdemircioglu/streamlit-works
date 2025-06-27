import sys
import os
import streamlit as st
import time
from utils.utils import display_menu_buttons
from utils.streamlit_helpers import smart_selectbox, smart_text_input, smart_text_area, smart_number_input, smart_date_input, render_clear_button_with_confirmation
# smart_multiselect ve smart_checkbox da var


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import my_functions

obj = my_functions.MyClass()

# When group changes, reset subgroup
def on_group_change():
    st.session_state.expense_subgroup = None  # ✅ This line resets subgroup



def show(navigate_to):
    st.title("Expense Entry")

    display_menu_buttons(navigate_to)

    # 1. Expense Date
    expense_date = smart_date_input("Expense Date", key="key_expense_date")

    # 2. Expense Type (used to filter banks)
    types = obj.get_expense_types()
    if types:
        type_dict = {name: gid for gid, name in types}
        selected_expense_type = smart_selectbox("Expense Type", options=list(type_dict.keys()), key="key_expense_type")
        selected_expense_type_id = type_dict[selected_expense_type]

    # 3. Expense Group
    groups = obj.get_expense_groups()  # should return [(id, name), ...]
    if groups:
        group_dict = {name: gid for gid, name in groups}
        
        # Determine index based on session state (defaults to first option if cleared)        
        selected_group_name = smart_selectbox("Expense Group", options=list(group_dict.keys()), key="key_expense_group")
        selected_group_id = group_dict[selected_group_name]


        # 4. Expense Subgroup (based on selected group)
        subgroups = obj.get_subgroups_by_group_id(selected_group_id)
        if subgroups:
            subgroup_dict = {name: sid for sid, name in subgroups}

            # Determine index based on session state (defaults to first option if cleared)
            selected_subgroup_name = smart_selectbox("Expense Subgroup", options=list(subgroup_dict.keys()), key="key_expense_subgroup")
            selected_subgroup_id = subgroup_dict[selected_subgroup_name]
        else:
            st.warning("No subgroups found for selected group.")
            selected_subgroup_id = None

    else:
        st.warning("No expense groups defined.")
        selected_group_id = None
        selected_subgroup_id = None


    # 5. Place & Detail
    expense_place = smart_text_input("Expense Place", key="key_expense_place")
    expense_detail = smart_text_input("Expense Detail", key="key_expense_detail")

    
    # 6. Amount
    expense_amount = smart_number_input("Expense Amount", min_value=0.0, step=0.01, format="%.2f", key="key_expense_amount")

    
    # 7. Installment Info
    installment_options = ["No", "Yes"]
    installment_status = smart_selectbox("Is it an Installment?", options=installment_options, key="key_installment_status")

    # Conditional fields based on selection
    if installment_status == "Yes":
        installment_count = smart_number_input("Total Installments",  default=2, min_value=2, step=1, format="%d", key="key_installment_count")
        no_of_installment = smart_text_input("Which Installment (e.g. 2/6)", key="key_no_of_installment")
    else:
        installment_count = 0
        no_of_installment = None


    # 8. Bank/Account Selection (based on expense type)
    banks = obj.get_bank_details_by_type(selected_expense_type)
    if banks:
        bank_display_dict = {f"{bank} - {detail}": bid for bid, bank, detail in banks}
        selected_bank_label = smart_selectbox("Select Bank / Account", options=list(bank_display_dict.keys()), key="key_bank_detail")
        selected_bank_id = bank_display_dict[selected_bank_label]
    else:
        selected_bank_id = None
        st.info("No bank/account found for this type.")


    # 9. Note
    expense_note = smart_text_area("Notes", height=80, key="key_expense_note")


    # --- Submit Button ---
    if st.button("Save Expense"):
        if not all([expense_date, selected_expense_type, selected_group_id, selected_subgroup_id, expense_amount > 0]):
            st.warning("Please fill in all required fields.")
        elif installment_status == "Yes" and not no_of_installment.strip():
            st.warning("Please fill in all required fields.")
        else:
            success = obj.insert_expense(
                expense_date=str(expense_date),
                expense_type=selected_expense_type_id,
                expense_group=selected_group_id,
                expense_subgroup=selected_subgroup_id,
                expense_place=expense_place.strip(),
                expense_detail=expense_detail.strip(),
                expense_amount=expense_amount,
                installment_status=installment_status,
                installment_count=installment_count,
                no_of_installment=no_of_installment,
                bank_id=selected_bank_id,
                expense_note=expense_note.strip()
            )
            if success:
                st.success("Expense entry saved.")
                time.sleep(1) # Screen doesn't show the st.success info because it is too fast.
                st.rerun()
            else:
                st.error("Something went wrong while saving.")


    """if st.button("Clear All Fields"):
        for key in [
            "key_expense_date", "key_expense_type", "key_expense_group", "key_expense_subgroup", "key_expense_place",
            "key_expense_detail", "key_expense_amount", "key_installment_status", "key_installment_count", "key_no_of_installment",
            "key_bank_detail", "key_expense_note"
        ]:
            st.session_state.pop(key, None)  # clears if key exists
            st.success("Form cleared.")
        st.rerun()"""
    

    form_keys = [
        "key_expense_date", "key_expense_type", "key_expense_group", "key_expense_subgroup",
        "key_expense_place", "key_expense_detail", "key_expense_amount",
        "key_installment_status", "key_installment_count", "key_no_of_installment",
        "key_bank_detail", "key_expense_note"
    ]

    render_clear_button_with_confirmation(form_keys)






