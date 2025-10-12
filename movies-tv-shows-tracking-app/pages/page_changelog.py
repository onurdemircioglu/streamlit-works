import streamlit as st
from utils.utils import display_menu_buttons

""" Format bu
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

def show(navigate_to):
    st.title("📜 Changelog")

    display_menu_buttons(navigate_to)

    changelog = [
        {
            "date": "2025-10-12",
            "changes": {
                "Added": [
                    "Before inserting OTHER_LINKS table, a duplication check added",
                    "On Search Page, an About section (expander) added"
                ],
                "Changed": [
                    "On Bulk Insert Page, there have been some changes for action map (new status and existing status)."
                ],
                "Fixed": [
                    "When it a new record with other (watch etc.) link, it only inserted the new record, not the link. Now they are inserted at the same time.",
                    "On Search Page, unique key error fixed"
                ]
            }
        },
        {
            "date": "2025-08-10",
            "changes": {
                "Fixed": [
                    "Dataframes was showing the old data after inserting/updating record. Added a refresh data commanda after insert/update before rerun() on TV Shows Page",
                    "On TV Shows Page, after editing New Min Episode No field, there was a slight refresh/tab switch problem for the New Max Episode No field",
                    "Latest Watched Episode No calculation on TV Shows Page"
                ]
            }
        },

        {
            "date": "2025-06-15",
            "changes": {
                "Added": ["Initial changelog page added to app."],
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



    #st.markdown("2025-06-15: Added a changelog page")

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/






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