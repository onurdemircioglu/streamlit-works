import streamlit as st
from utils.utils import display_menu_buttons

def show(navigate_to):
    st.title("📜 Changelog")

    display_menu_buttons(navigate_to)    

    changelog = [
        {
            "date": "2025-06-21",
            "changes": {
                "Added": [
                    "Clear All Fields (Reset Form) button added on Expense Entry page ",
                    "Smart selection functions created for the default values on Expense Entry page (after clearing the form)",
                    "Constraint check: if installment status is Yes then no of installment must be filled.",
                    "Confirmation checkbox before clearing the form (preventing accidental wipes)",
                    "Latest Entries Page created which shows the last 30 records (based on ID, not the Expense Date)",
                    "Basic Montly Expense Trend Chart on Dashboard Page",
                    "Basic Montly Expense Trend Table on Dashboard Page"
                ],
                "Changed": [
                    "Expense Entry page and the code modified based on recently created lookup tables",
                    "IS_ACTIVE column added in TBL_EXPENSES table",
                    "Uniqueness check updated BANK_NAME and DETAIL_NAME both on TBL_BANKS_LKP and Manage Banks page",
                    "Regarding uniqueness check on TBL_BANKS_LKP"
                ]
            }
        },


        {
            "date": "2025-06-20",
            #"version": "v0.2",
            "changes": {
                "Added": [
                    "Manage Banks tab created",
                    "TBL_BANKS_LKP table created",
                    "Bank and bank detail functionalities (insert, rename, duplicate check, soft delete, restore)",
                    "Bank and expense type association created"
                    ]
            }
        },

        {
            "date": "2025-06-19",
            #"version": "v0.2",
            "changes": {
                "Added": [
                    "Manage Types tab created",
                    "TBL_EXPENSE_TYPES_LKP table created",
                    "Expense Type functionalities (insert, rename, duplicate check, soft delete, restore)",
                    ],
                "Changed": [
                    "Order of function in Manage Groups tab"
                ]
            }
        },

        {
            "date": "2025-06-18",
            #"version": "v0.2",
            "changes": {
                "Added": [
                    "Expense Group functionalities (insert, rename, duplicate check, soft delete, restore)",
                    "Expense Subgroup functionalities (insert, rename, duplicate check, soft delete, restore)",
                    "Unique constraint check for TBL_EXPENSE_GROUPS_LKP and TBL_EXPENSE_SUBGROUPS_LKP tables",
                    "IS_ACTIVE column added for soft delete functionality in TBL_EXPENSE_GROUPS_LKP and TBL_EXPENSE_SUBGROUPS_LKP tables",
                    ],
                "Changed": [
                    "Settings tab renamed to Manage Groups"
                ]
            }
        },

        {
            "date": "2025-06-17",
            #"version": "v0.2",
            "changes": {
                "Added": [
                    "TBL_EXPENSE_GROUPS_LKP table created",
                    "TBL_EXPENSE_SUBGROUPS_LKP table created",
                    "Settings tab created"
                    ],
                "Changed": [
                    "EXPENSE_GROUP and EXPENSE_SUBGROUP column formats converted to integer from text to be align with lookup tables."
                ]
            }
        },

        {
            "date": "2025-06-15",
            #"version": "v0.1",
            "changes": {
                "Added": [
                    "Writing new record (basic) into database",
                    "Change Log page",
                    "Expense Entry page",
                    "Dashboard page",
                    "Database objects",
                    "Project Started."
                ],
            }
        }
    ]



    for entry in changelog:
        #st.subheader(f"{entry['version']} — {entry['date']}")
        st.subheader(f"{entry['date']}")
        for section, items in entry["changes"].items():
            st.markdown(f"**{section}**")
            for item in items:
                st.markdown(f"- {item}")
            st.markdown("---")





"""
Format bu
        {
            "date": "2025-XX-YY",
            "version": "v1.4",
            "changes": {
                "Added": [
                    "New 'Interests' column with many-to-many database support.",
                    "Clear form button now works as expected."
                ],
                "Changed": [
                    "Improved layout for 'New Record' form using Streamlit columns."
                ],
                "Fixed": [
                    "Score date input bug where value wouldn't clear properly."
                ]
            }
        },
"""


"""
Versioning
Recommended Format: MAJOR.MINOR.PATCH
1.4.2
| Segment   | Meaning          | When to Increase                              |
| --------- | ---------------- | --------------------------------------------- |
| **MAJOR** | Breaking changes | Changes that are not backward compatible (e.g. Imcompatible API)     |
| **MINOR** | New features     | New features that are backward compatible     |
| **PATCH** | Fixes            | Bug fixes, performance tweaks, UI adjustments |

How You Might Use It
| Version | Description                                       |
| ------- | ------------------------------------------------- |
| `1.0.0` | First stable release                              |
| `1.1.0` | Added “Clear Form” button                         |
| `1.1.1` | Fixed clear form bug                              |
| `1.2.0` | Added “Interests” column with multiselect         |
| `2.0.0` | Major redesign or refactor of the database schema |

"""