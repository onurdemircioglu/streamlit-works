""" Format bu
        {
            "date": "2025-XX-YY",
            "version": "v1.4",
            "changes": {
                "Added": [
                    "None"
                ],
                "Changed": [
                    "None"
                ],
                "Fixed": [
                    "None"
                ]
            }
        },
        """

import streamlit as st
from utils.utils import display_menu_buttons

def show(navigate_to):
    st.title("📜 Changelog")

    display_menu_buttons(navigate_to)    



    changelog = [
        {
            "date": "2025-XX-YY",
            "version": "v1.4",
            "changes": {
                "Added": [
                    "Expense Distributor on Calculations Page"
                ],
                "Changed": [
                    "None."
                ],
                "Fixed": [
                    "None"
                ]
            }
        },
        {
            "date": "2025-07-26",
            "changes": {
                "Added": [
                    "None",
                ],
                "Changed": [
                    "When 'Show Future Expenses' selected Monthly Expenses chart title updates accordingly on Dashboard Page",
                    "When 'Show Future Expenses' selected Monthly Expenses by Period (Stacked by Category) table title updates accordingly on Dashboard Page",
                    "When 'Show Future Expenses' selected Monthly Totals Table title updates accordingly on Dashboard Page",
                    "When 'Show Future Expenses' selected Expense Breakdown pie chart title updates accordingly on Dashboard Page",
                    "Smart selection functions are implemented on other pages too",
                    "All data sources converted into REPORTABLE_EXPENSES view"
                ],
                "Fixed": [
                    "None"
                ]
            }
        },

        {
            "date": "2025-07-25",
            "changes": {
                "Added": [
                    "Add/Update/Delete income types added in Manage Incomes tab under Settings Page",
                    "Manage Incomes tab created in Settings Page (add/update/delete income)",
                    "A monthly trend stacked chart with category breakdown added on Dashboard Page",

                ],
                "Changed": [
                    "Newly added chart (monthly trend stacked chart with category breakdown) placed right of the Montly Expenses on Dashboard Page",
                    "Monthly Totals Table placed below the Monthly Expenses on Dashboard Page"
                ]
            }
        },

        {
            "date": "2025-07-23",
            "changes": {
                "Added": [
                    "IS_ACTIVE column added in TBL_INCOMES table"
                ]
            }
        },

        {
            "date": "2025-07-19",
            "changes": {
                "Added": [
                    "A toggle button added for charts on the Dashboard Page to include/exclude future expenses",
                    "Instead of using st.divider() to draw horizontal lines a more flexiable function (draw_separator) created using st.markdown and html"
                    
                ],
                "Changed": [
                    "The source of Monthly Expenses chart are changed to REPORTABLE_EXPENSES view (more compact and readable)",
                    "EXPENSE_MONTH column added into REPORTABLE_EXPENSES view in database"
                ]
            }
        },

        {
            "date": "2025-07-16",
            "changes": {
                "Added": [
                    "TBL_INCOMES table created for incomes",
                    "TBL_INCOMES_TYPES_LKP table create for income types"
                ]
            }
        },

        {
            "date": "2025-07-15",
            "changes": {
                "Added": [
                    "Settings Page created",
                    "Manage Groups, Manage Types, Manage Banks pages moved into Settings Page",
                ]
            }
        },

        {
            "date": "2025-07-14",
            "changes": {
                "Added": [
                    "Export page created for data exports",
                    "Net Present Value calculation added on Calculations Page"
                ]
            }
        },
        
        {
            "date": "2025-07-12",
            "changes": {
                "Added": [
                    "Calculations page created"
                ],
                "Changed": [
                    "REMINDERS page rearranged with adding functionality of editing reminders"
                ]
            }
        },

        {
            "date": "2025-06-29",
            "changes": {
                "Added": [
                    "TBL_REMINDERS table created for tracking dates (bills, payment etc.)",
                    "REMINDERS page created to insert/delete/update reminders",
                    "View and Filter Reminders section added on Dashboard Page (with All, Upcoming, Overdue, Done, Active filters and 'Marks as Done', 'Delete' functionalities) "
                ],
            }
        },

        {
            "date": "2025-06-28",
            "changes": {
                "Added": [
                    "An average line for Montly Expense Trend Chart on Dashboard Page",
                    "Show Month Average Line toggle button on Montly Expense Trend Chart on Dashboard Page (This is also dynamic based on the selection of number of months)",
                    "A percentage difference column from average (with in the Montly Expense Trend Table on Dashboard Page (🔴 Red if above average (overspending), 🟢 Green if below average (under control))",
                    "Top x months with the highest total expenses are shown in red bar with user input (capped with number of month selection)",
                    "st.slider added for the how many months are shown on the chart",
                    "Month to month (MoM) change added on Montly Expense Trend Table on Dashboard Page",
                    "Year on year (YoY) change added on Montly Expense Trend Table on Dashboard Page",
                    "Year to date (YtD) change added on Montly Expense Trend Table on Dashboard Page",
                    "12 Months Moving Average line added on Montly Expense Trend Chart on Dashboard Page",
                    "12 Months Moving Average amount added on Montly Expense Trend Table on Dashboard Page",
                    "REPORTABLE_EXPENSES view created on database to ease the data retrieving process",
                    "'Select a Month for Detailed Breakdown' added below the Trend chart on Dashboard Page. This shows selected month's total expsenses by expense group with percentage and mini pie chart",
                    "Future installments summary on Dashboard Page (If there is none it writes 'There is no future dated expense.')"
                ],
                "Changed": [
                    "Montly Expense Trend Chart on Dashboard Page is converted into bar chart format",
                    "Montly Expense Trend Chart on Dashboard Page recreated with Altair (st.altair_chart)",
                    "'Monthly Expenses (Last x Months) chart title now uses selection of number of months as input",
                    "Columns are renamed on Montly Expense Trend Table on Dashboard Page"
                ]
            }
        },

        {
            "date": "2025-06-21",
            "changes": {
                "Added": [
                    "Clear All Fields (Reset Form) button added on Expense Entry page ",
                    "Smart selection functions created for the default values on Expense Entry page (after clearing the form)",
                    "Constraint check: if installment status is Yes then no of installment must be filled.",
                    "Confirmation checkbox before clearing the form (preventing accidental wipes)",
                    "Latest Entries Page created which shows the last 30 records (based on ID, not the Expense Date)",
                    "Montly Expense Trend Chart on Dashboard Page",
                    "Montly Expense Trend Table on Dashboard Page"
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








"""Versioning
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