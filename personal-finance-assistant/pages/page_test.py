import streamlit as st
import pandas as pd
from datetime import date
import time
import altair as alt
import math
from utils.utils import display_menu_buttons
from utils import my_functions


obj = my_functions.MyClass()



def show_page_contents():
        
    # Access stored DataFrames
    if (
        "expenses_df" in st.session_state 
        or "reportable_expenses_df" in st.session_state
    ):
        # Metrics
    
# **************************************************************** PREPARING DATA FOR CHART - START **************************************************************** #
        monthly_expenses_graph_data = st.session_state.reportable_expenses_df.copy()

        # Convert date column to datetime
        monthly_expenses_graph_data["EXPENSE_DATE"] = pd.to_datetime(monthly_expenses_graph_data["EXPENSE_DATE"], format="%Y-%m-%d") # errors="coerce" will turn any truly invalid dates into NaT instead of crashing

        # Create year-month column
        #monthly_expenses_graph_data["YEAR_MONTH"] = monthly_expenses_graph_data["EXPENSE_DATE"].dt.to_period("M").astype(str)
        
        # Converting the EXPENSE_AMOUNT into corret format before group and sum
        monthly_expenses_graph_data["EXPENSE_AMOUNT"] = (
            monthly_expenses_graph_data["EXPENSE_AMOUNT"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        # Group and sum
        #monthly_totals = monthly_expenses_graph_data.groupby("YEAR_MONTH")["EXPENSE_AMOUNT"].sum().reset_index()
        monthly_totals = monthly_expenses_graph_data.groupby( ["EXPENSE_PERIOD", "EXPENSE_YEAR", "EXPENSE_MONTH"] )["EXPENSE_AMOUNT"].sum().reset_index()
        monthly_totals["EXPENSE_AMOUNT"] = pd.to_numeric(monthly_totals["EXPENSE_AMOUNT"], errors="coerce").fillna(0)
        monthly_totals["EXPENSE_YEAR"] = pd.to_numeric(monthly_totals["EXPENSE_YEAR"], errors="coerce").fillna(0)
        monthly_totals["% FROM PREV"] = monthly_totals["EXPENSE_AMOUNT"].pct_change() * 100
        monthly_totals["% FROM PREV"] = monthly_totals["% FROM PREV"].round(1)


        # 12 Months Moving average
        monthly_totals["12M_MA"] = (monthly_totals["EXPENSE_AMOUNT"].rolling(window=12, min_periods=1).mean().round(1))

        # Calculate Year-over-Year Change
        #monthly_totals["YEAR"] = monthly_totals["YEAR_MONTH"].str[:4].astype(int)
        #monthly_totals["MONTH"] = monthly_totals["YEAR_MONTH"].str[5:7].astype(int)

        # Create previous year dataframe
        #prev_year_df = monthly_totals[["YEAR", "MONTH", "EXPENSE_AMOUNT"]].copy()
        prev_year_df = monthly_totals[["EXPENSE_YEAR", "EXPENSE_MONTH", "EXPENSE_AMOUNT"]].copy()
        #prev_year_df["YEAR"] += 1  # shift year forward so we can match later
        prev_year_df["EXPENSE_YEAR"] += 1  # shift year forward so we can match later
        prev_year_df.rename(columns={"EXPENSE_AMOUNT": "EXPENSE_AMOUNT_LAST_YEAR"}, inplace=True)


        # Merge back with current data
        monthly_totals = monthly_totals.merge(
            prev_year_df,
            #on=["YEAR", "MONTH"],
            on=["EXPENSE_YEAR", "EXPENSE_MONTH"],
            how="left"
        )


        # Calculate Year-over-Year % Change
        monthly_totals["YoY_CHANGE"] = (
            (monthly_totals["EXPENSE_AMOUNT"] - monthly_totals["EXPENSE_AMOUNT_LAST_YEAR"])
            / monthly_totals["EXPENSE_AMOUNT_LAST_YEAR"]
        ) * 100

        monthly_totals["YoY_CHANGE"] = monthly_totals["YoY_CHANGE"].round(1)

        
        # Calculate Year-to-Date (YtD) Change
        #dec_totals = monthly_totals[monthly_totals["MONTH"] == 12][["YEAR", "EXPENSE_AMOUNT"]].copy()
        dec_totals = monthly_totals[monthly_totals["EXPENSE_MONTH"] == 12][["EXPENSE_YEAR", "EXPENSE_AMOUNT"]].copy()
        dec_totals.columns = ["YEAR_DEC", "DEC_EXPENSE"]
        dec_totals["YEAR_DEC"] += 1  # so 2024 Dec becomes 2025 reference

        # Merge back with current data
        monthly_totals = monthly_totals.merge(
            dec_totals,
            #left_on="YEAR",
            left_on="EXPENSE_YEAR",
            right_on="YEAR_DEC",
            how="left"
        )

        monthly_totals["YTD_CHANGE"] = (
            (monthly_totals["EXPENSE_AMOUNT"] - monthly_totals["DEC_EXPENSE"])
            / monthly_totals["DEC_EXPENSE"]
        ) * 100

        monthly_totals["YTD_CHANGE"] = monthly_totals["YTD_CHANGE"].round(1)


        # TODO: Do I need this? And why?
        def format_label(row):
            expense = f"{row['EXPENSE_AMOUNT']:,.0f} ₺"
            pct = row['% FROM PREV']
            if pd.isna(pct):
                return expense
            sign = "+" if pct > 0 else ""
            return f"{expense}\n({sign}{pct:.1f}%)"

        monthly_totals["MoM %"] = monthly_totals.apply(format_label, axis=1)
        
        # Average line on the chart
        show_avg_line = st.toggle("Show Month Average Line", value=True)

        # Toggle to include/exclude future expenses
        show_future = st.checkbox("Show Future Expenses", value=False)        
        
        # Number of months selection on chart (min 6, max 36)
        chart_slider = st.slider("Months Selection", min_value=6, max_value=36, value=13, step=1)


        
        monthly_totals_filtered = (
            #monthly_totals.sort_values("YEAR_MONTH")
            monthly_totals.sort_values("EXPENSE_PERIOD")
            .tail(chart_slider)
            .copy()
        )

        # To filter future expenses
        if not show_future:
            today = pd.Timestamp.today()
            monthly_totals_filtered = monthly_totals_filtered[pd.to_datetime(monthly_totals_filtered["EXPENSE_DATE"]) <= today]


        # To select how many months for the highest expense selection
        top_x_slider = st.slider("Top Months Selection", min_value=1, max_value=round(int(chart_slider/2),0)+1, value=1, step=1)

        # Dynamic total expense value for the Y axis on chart
        max_val = monthly_totals_filtered["EXPENSE_AMOUNT"].max()
        rounded_max = math.ceil(max_val / 1000) * 1000


        # Side-by-side layout (chart on the left, chart data on the right)
        col_chart, col_table = st.columns([1, 1])

        # Calculate average and % diff
        avg_value = monthly_totals_filtered["EXPENSE_AMOUNT"].mean()
        monthly_totals_filtered["% FROM AVG"] = ((monthly_totals_filtered["EXPENSE_AMOUNT"] - avg_value) / avg_value) * 100




        ##############################################################################################################################
        # Monthly Trend Chart Breakdown by Expense Groups 
        graph_data_v2 = st.session_state.reportable_expenses_df.copy()

        # --- Group by MONTH + CATEGORY (Expense Group) ---
        #graph_data_v2["MONTH"] = pd.to_datetime(graph_data_v2["EXPENSE_DATE"]).dt.to_period("M").astype(str)

        # Converting the EXPENSE_AMOUNT into corret format before group and sum
        graph_data_v2["EXPENSE_AMOUNT"] = (
            graph_data_v2["EXPENSE_AMOUNT"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        grouped_df_v2 = (
            graph_data_v2.groupby(["EXPENSE_PERIOD", "EXPENSE_GROUP"], as_index=False)["EXPENSE_AMOUNT"]
            .sum()
            .rename(columns={"EXPENSE_AMOUNT": "TOTAL_AMOUNT"})
        )

        # --- Pivot for readability (not strictly required for Altair, but useful) ---
        pivot_df = grouped_df_v2.pivot(index="EXPENSE_PERIOD", columns="EXPENSE_GROUP", values="TOTAL_AMOUNT").fillna(0)
        pivot_df = pivot_df.reset_index()

        # --- Convert to long format for Altair ---
        long_df = pivot_df.melt(id_vars="EXPENSE_PERIOD", var_name="Category", value_name="Amount")


        # ✅ Convert to datetime for proper sorting & filtering
        long_df["EXPENSE_PERIOD"] = pd.to_datetime(long_df["EXPENSE_PERIOD"], format="%Y-%m")

        # --- Slider for Months Selection ---
        #chart_slider = st.slider("Months Selection", min_value=6, max_value=36, value=13, step=1)


        # ✅ Filter for the latest X months
        latest_months = long_df["EXPENSE_PERIOD"].dropna().sort_values(ascending=False).unique()[:chart_slider]
        filtered_df = long_df[long_df["EXPENSE_PERIOD"].isin(latest_months)]


        # --- Sort chronologically (ascending order for charts) ---
        filtered_df = filtered_df.sort_values(by="EXPENSE_PERIOD")




# **************************************************************** PREPARING DATA FOR CHART - END **************************************************************** #



# **************************************************************** CREATING CHART - START **************************************************************** #

        # Creating Bar Chart
        with col_chart:
            monthly_totals_filtered["BAR_COLOR"] = "#007ACC"  # default blue

            # Find top x by expense and color it
            topx_idx = monthly_totals_filtered["EXPENSE_AMOUNT"].nlargest(top_x_slider).index
            monthly_totals_filtered.loc[topx_idx, "BAR_COLOR"] = "#FF4C4C"  # red for top 5

            # Altair base chart
            base = alt.Chart(monthly_totals_filtered).mark_bar().encode(
                x=alt.X("EXPENSE_PERIOD:N", title="Month", sort=None, axis=alt.Axis(labelAngle=-40)),
                y=alt.Y(
                    "EXPENSE_AMOUNT:Q",
                    title="Total Expense",
                    scale=alt.Scale(domain=[0, rounded_max]),
                    axis=alt.Axis(labelFontSize=10, titleFontSize=12)
                ),
                color=alt.Color("BAR_COLOR:N", scale=None),  # use predefined color, no gradient
                tooltip=[
                    alt.Tooltip("EXPENSE_PERIOD", title="Month"),
                    alt.Tooltip("EXPENSE_AMOUNT", format=",.0f", title="Amount (₺)"),
                    alt.Tooltip("% FROM AVG", format=".1f", title="% From Avg")
                ]
            ).properties(
                width=800,
                height=450,
                title=(f"Monthly Expenses (Last {chart_slider} Months)")
                )
            
            # 12 Months Moving Average
            ma_line = alt.Chart(monthly_totals_filtered).mark_line(
                color="orange", strokeWidth=2
            ).encode(
                x="EXPENSE_PERIOD:N",
                y="12M_MA:Q"
            )
            
            labels = alt.Chart(monthly_totals_filtered).mark_text(
                dy=-15,  # move label above bar
                fontSize=13,
                color="black"
            ).encode(
                x=alt.X("EXPENSE_PERIOD:N", title="Month", sort=None, axis=alt.Axis(labelAngle=-40)),
                y=alt.Y("EXPENSE_AMOUNT:Q"),
                text=alt.Text("EXPENSE_AMOUNT:Q", format=",.0f")
                #text=alt.Text("MoM %:N")
            )

            # 12 Months Moving Average label
            ma_label = alt.Chart(monthly_totals_filtered.tail(1)).mark_text(
                text="12M Avg",
                color="orange",
                dx=5, dy=-5,
                fontSize=10
            ).encode(
                x="EXPENSE_PERIOD:N",
                y="12M_MA:Q"
            )

            # Showin average line
            if show_avg_line:
                avg_line = alt.Chart(pd.DataFrame({"y": [avg_value]})).mark_rule(
                    color="red", strokeDash=[4, 4]
                ).encode(y="y:Q")
                avg_label = alt.Chart(pd.DataFrame({"y": [avg_value]})).mark_text(
                    text=f"Avg: {avg_value:,.0f} ₺",
                    align="right", baseline="bottom",
                    dx=-5, dy=-5,
                    color="red",
                    fontSize=10
                ).encode(y="y:Q", x=alt.value(480))
                chart = base + labels + ma_line + ma_label + avg_line + avg_label
            else:
                chart = base + labels + ma_line + ma_label


            # Display chart
            st.altair_chart(chart, use_container_width=False)

# **************************************************************** CREATING CHART - END **************************************************************** #


            # To draw divider
            obj.draw_separator(color="#01055b", thickness=1, radius=12)



# **************************************************************** TABLE DATA OF CHART - START **************************************************************** #

        """# ---- Table ----
        with col_table:
            display_df = monthly_totals_filtered.drop(columns=["BAR_COLOR", "MoM %"]).copy()
            display_df["EXPENSE_AMOUNT"] = display_df["EXPENSE_AMOUNT"].apply(lambda x: f"{x:,.0f}")
            display_df["12M_MA"] = display_df["12M_MA"].apply(lambda x: f"{x:,.0f}")
            display_df["% FROM AVG"] = monthly_totals_filtered["% FROM AVG"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "-")
            display_df["% FROM PREV"] = monthly_totals_filtered["% FROM PREV"].apply(
                lambda x: f"{x:+.1f}%" if pd.notna(x) else "-"
            )


            display_df["YoY Change (%)"] = display_df["YoY_CHANGE"].apply(
                lambda x: f"{x:+.1f}%" if pd.notna(x) else "-"
            )

            display_df["YtD Change (%)"] = display_df["YTD_CHANGE"].apply(
                lambda x: f"{x:+.1f}%" if pd.notna(x) else "-"
            )

            # Then drop the raw calc columns if desired
            display_df.drop(columns=["YEAR", "MONTH", "YoY_CHANGE", "YEAR_DEC", "DEC_EXPENSE", "YTD_CHANGE", "EXPENSE_AMOUNT_LAST_YEAR"], inplace=True)


            # Renaming columns
            display_df.rename(columns={
                "% FROM PREV": "MoM Change (%)",
                "YEAR_MONTH":"Period",
                "EXPENSE_AMOUNT":"Expense Amount",
                "% FROM AVG":"Change From Avg (%)",
                "12M_MA": "12 Months Avg"
                }, inplace=True)


            # Formatting the percentage data
            def highlight_percent(val):
                try:
                    percent = float(val.strip('%').replace('+', '').replace(',', '.'))
                    if percent > 0:
                        return "color: red"
                    elif percent < 0:
                        return "color: green"
                    else:
                        return ""
                except:
                    return ""

            styled_df = display_df.style.apply(
                lambda col: [highlight_percent(v) for v in col] if col.name in (
                    "Change From Avg (%)",
                    "MoM Change (%)",
                    "YoY Change (%)",
                    "YtD Change (%)"
                    ) else [""] * len(col),
                axis=0
            )


            st.markdown("#### 📋 Monthly Totals Table")
            st.dataframe(styled_df, use_container_width=True, hide_index=True)"""

# **************************************************************** TABLE DATA OF CHART - END **************************************************************** #



def show(navigate_to):
    st.title("Dashboard - Test")

    display_menu_buttons(navigate_to)

    show_page_contents()









