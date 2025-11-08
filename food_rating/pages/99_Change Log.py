import streamlit as st

st.title("📜 Changelog")

changelog = [
    {
        "date": "2025-11-08",
        "changes": {
            "Added": [
                "Add Food Rating Page (with new Store/Category entry functionalities)",
                {
                    "View Ratings Page:": [
                        "Filters: Store, Category, Start Date, End Date",
                        "Showing Existing Ratings",
                        "Average rating metrics",
                        {
                            "3 charts:": [
                                "Bar Chart: Top-rated Foods",
                                "Scatter Plot: Taste vs Price",
                                "Monthly Trend (Avg Score)"
                            ]
                        },
                    ]
                },

                {
                    "Statistics Page:": [
                        "Filters: Store, Category, Start Date, End Date",
                        "Overall Metrics",
                        "Mini Rating Count Charts by Date, Store and Category",
                        "Top-rated Stores/Categories Chart",
                        "Store/Category Comparison Chart",
                        "Taste vs Price Heatmap by Category",
                        "Trend Analysis per Food with filters (Store, Category, Food Name, Start Date, End Date)",
                        "Category Comparisons (with Filter by Store (optional))"
                        
                    ]
                },
                {
                    "Statistics Page:": [
                        "Unrated Foods with filters (Number of months, Store, Category, Food Name)"                        
                    ]
                },

    
                
                
                
                
            ],
            "Changed": [
                "None"
            ],
            "Fixed": [
                "None"
            ]
        }
    }
]




def render_items(items, indent=0):
    for item in items:
        if isinstance(item, dict):
            for k, v in item.items():
                st.markdown(f"{'&nbsp;'*indent*16}- **{k}**", unsafe_allow_html=True)
                render_items(v, indent+1)
        else:
            st.markdown(f"{'&nbsp;'*indent*16}- {item}", unsafe_allow_html=True)

for entry in changelog:
    st.subheader(f"{entry['date']}")
    for section, items in entry["changes"].items():
        st.markdown(f"**{section}**")
        render_items(items)
        st.markdown("---")