import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from utils.utils import display_menu_buttons

def trend_report():
        
    # Access stored DataFrames
    if (
        "expenses_df" in st.session_state 
    ):
        # Metrics
    

        
        # Creating graphic 
        graph_data = st.session_state.expenses_df.copy()

        # Step 1: Convert date column to datetime
        #graph_data["EXPENSE_DATE"] = pd.to_datetime(graph_data["EXPENSE_DATE"])
        graph_data["EXPENSE_DATE"] = pd.to_datetime(graph_data["EXPENSE_DATE"], format="%Y-%m-%d") # errors="coerce" will turn any truly invalid dates into NaT instead of crashing
        #graph_data["EXPENSE_DATE"] = pd.to_datetime(graph_data["EXPENSE_DATE"], errors="coerce")
        #graph_data["EXPENSE_DATE"] = pd.to_datetime(graph_data["EXPENSE_DATE"], format="%Y-%m-%d", errors="coerce")

        # Filter for last 13 months
        today = pd.to_datetime(datetime.today().date())
        cutoff_date = today - relativedelta(months=13)

        graph_data = graph_data[graph_data["EXPENSE_DATE"] >= cutoff_date]


        # Step 2: Create year-month column
        graph_data["YEAR_MONTH"] = graph_data["EXPENSE_DATE"].dt.to_period("M").astype(str)
        
        
        # Step 3: Converting the EXPENSE_AMOUNT into corret format before group and sum
        graph_data["EXPENSE_AMOUNT"] = (
            graph_data["EXPENSE_AMOUNT"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        # Step 4: Group and sum
        monthly_totals = graph_data.groupby("YEAR_MONTH")["EXPENSE_AMOUNT"].sum().reset_index()
        
        # Step 5: Plot

        # Create side-by-side layout
        col_chart, col_table = st.columns([1, 1])  # equal width

        # ---- Left: Chart ----
        with col_chart:
            fig, ax = plt.subplots(figsize=(6, 2.5))

            ax.plot(
                monthly_totals["YEAR_MONTH"],
                monthly_totals["EXPENSE_AMOUNT"],
                marker="o",
                linewidth=1.5,
                color="#007ACC"
            )

            for i, row in monthly_totals.iterrows():
                ax.text(i, row["EXPENSE_AMOUNT"], f"{row['EXPENSE_AMOUNT']:.0f}", ha="center", va="bottom", fontsize=7)

            ax.set_title("Monthly Expenses", fontsize=10)
            ax.set_xlabel("Year-Month", fontsize=8)
            ax.set_ylabel("₺", fontsize=8)
            plt.xticks(rotation=45, fontsize=7)
            plt.yticks(fontsize=7)
            plt.tight_layout()

            st.pyplot(fig)

        # ---- Right: Table ----
        with col_table:
            # Optional: Format expense values
            display_df = monthly_totals.copy()
            display_df["EXPENSE_AMOUNT"] = display_df["EXPENSE_AMOUNT"].apply(lambda x: f"{x:,.0f}")

            st.markdown("#### 📋 Monthly Totals Table")
            st.dataframe(display_df, use_container_width=True, hide_index=True)



def show(navigate_to):
    st.title("Dashboard")

    display_menu_buttons(navigate_to)

    trend_report()





