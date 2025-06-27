
# Hiç başlanmadıIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

import streamlit as st
from utils.utils import display_menu_buttons

def entry_form_actions():
    if "form_loaded" not in st.session_state:
        st.session_state["form_loaded"] = False

    #Loading the Form:
    if not st.session_state["form_loaded"]:
        if st.button("Load Form"):
            st.session_state["form_loaded"] = True
            st.rerun()
    else:
        st.write("Here's the expense entry form!")
        
        with st.form(key="data_entry_form",border=True):
                
                expense_type_options = ["CREDIT CARD", "ACCOUNT", "CASH"]
                
                expense_group_options = {
                    "ENTERTAINMENT": ["MOVIES", "THEATER", "BAR", "OTHER"],
                    "FODD": ["BREAKFAST/LUNCH/DINNER", "GROCERY/MARKET", "CAFE/PATISSERIE", "OTHER"],
                    "HOUSING": ["ELECTRICITY", "GAS", "INTERNET", "LANDLINE PHONE", "MAINTENANCE", "MONTHLY FIXED FEES", "RENT", "TV", "WATER", "BUILDING EXPENSES", "OTHER"],
                    "GIFTS AND DONATIONS": ["CHARITY", "DONATIONS", "GIFTS", "OTHER"],
                    "INSURANCE": ["AUTO INSURANCE", "HEALTH INSURANCE", "LIFE INSURANCE", "RETIREMENT AGREEMENT", "OTHER"],
                    "LOANS": ["AUTO", "MORTGAGE", "STUDENT", "OTHER"],
                    "PERSONAL CARE": ["CELL PHONE", "CHILDCARE", "CLOTHING", "EDUCATION", "ELECTRONICS", "MEDICAL EXPENSES", "PETS", "GYM MEMBERSHIP", "OTHER"],
                    "TRANSPORTATION": ["AUTO EXPENSES", "FUEL", "PARKING", "PASS", "TAXI", "FLIGHT", "FERRY", "OTHER"],
                    "LEGAL": ["OTHER"],
                    "TAXES": ["OTHER"],
                    "OTHER": ["OTHER"]
                    }
                # Get unique values
                unique_title_type_options = sorted(set(sum(expense_group_options.values(), [])))

                expense_date = st.date_input("Expense Date", key="expense_date")
                
                expense_type = st.radio(
                "Select Type",
                expense_type_options,
                horizontal=True,  # Makes options appear inline
                index=0,  # Default: Credit Card
                key="expense_type"
                )

                expense_group = st.selectbox(
                "Select Expense Group",
                list(expense_group_options.keys()),
                #horizontal=True,  # Makes options appear inline
                index=0,  # Default: "ENTERTAINMENT"
                key="expense_group"
                )


                """# If this is in the st.form it doesn't dynamically update. (If it is a standalone or outside the form then it does)
                expense_sub_group = st.selectbox(
                "Select Expense Subgroup",
                unique_title_type_options,
                index=unique_title_type_options.index("OTHER"),
                key="expense_sub_group"
                )"""


                # Initialize session state keys
                if "expense_group" not in st.session_state:
                    st.session_state.expense_group = list(expense_group_options.keys())[0]

                if "expense_subgroup" not in st.session_state:
                    st.session_state.expense_subgroup = None

                # When group changes, reset subgroup
                def on_group_change():
                    st.session_state.expense_subgroup = None  # ✅ This line resets subgroup

                # Expense Group selection
                expense_group = st.selectbox(
                    "Select Expense Group",
                    options=list(expense_group_options.keys()),
                    index=list(expense_group_options.keys()).index(st.session_state.expense_group),
                    key="expense_group",
                    on_change=on_group_change
                )

                # Expense Subgroup selection based on selected group
                subgroups = expense_group_options.get(expense_group, [])
                expense_subgroup = st.selectbox(
                    "Select Expense Subgroup",
                    options=subgroups,
                    key="expense_subgroup"
                )




                submitted = st.form_submit_button("Insert Record")

                #st.form_submit_button(label="Submit", help=None, on_click=None, args=None, kwargs=None, *, type="secondary", icon=None, disabled=False, use_container_width=False)
                if submitted:
                    # Inserting new record
                    new_record_result = obj.insert_new_record(
                        imdb_in
                        ,record_type, record_title_type
                        ,original_title, primary_title
                        ,record_status, release_year
                        ,record_score, score_date
                        ,imdb_rating, imdb_rating_count, imdb_genres_str
                        ,watch_grade
                        )
                    
                    if new_record_result > 0:
                        toast_message = st.toast(f"✅ Successfully inserted record, ID: {new_record_result}")
                    else:
                        toast_message = st.warning("Something is wrong")

    # Resetting the Form:
    if st.button("Clear My Form"): # Inspired by https://discuss.streamlit.io/t/solution-how-to-reset-a-streamlit-form-when-clear-on-submit-isnt-an-option/87508
        # Remove the key that shows the form
        del st.session_state["form_loaded"]
        st.rerun()

def show(navigate_to):
    st.title("Expense Entry")

    display_menu_buttons(navigate_to)

    entry_form_actions()