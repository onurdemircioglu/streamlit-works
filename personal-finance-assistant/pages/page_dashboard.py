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
    ):
        # Metrics
    
# **************************************************************** PREPARING DATA FOR CHART - START **************************************************************** #
        graph_data = st.session_state.expenses_df.copy()

        # Convert date column to datetime
        graph_data["EXPENSE_DATE"] = pd.to_datetime(graph_data["EXPENSE_DATE"], format="%Y-%m-%d") # errors="coerce" will turn any truly invalid dates into NaT instead of crashing

        # Create year-month column
        graph_data["YEAR_MONTH"] = graph_data["EXPENSE_DATE"].dt.to_period("M").astype(str)
        
        # Converting the EXPENSE_AMOUNT into corret format before group and sum
        graph_data["EXPENSE_AMOUNT"] = (
            graph_data["EXPENSE_AMOUNT"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        # Group and sum
        monthly_totals = graph_data.groupby("YEAR_MONTH")["EXPENSE_AMOUNT"].sum().reset_index()
        monthly_totals["EXPENSE_AMOUNT"] = pd.to_numeric(monthly_totals["EXPENSE_AMOUNT"], errors="coerce").fillna(0)
        monthly_totals["% FROM PREV"] = monthly_totals["EXPENSE_AMOUNT"].pct_change() * 100
        monthly_totals["% FROM PREV"] = monthly_totals["% FROM PREV"].round(1)

        # 12 Months Moving average
        monthly_totals["12M_MA"] = (monthly_totals["EXPENSE_AMOUNT"].rolling(window=12, min_periods=1).mean().round(1))

        # Calculate Year-over-Year Change
        monthly_totals["YEAR"] = monthly_totals["YEAR_MONTH"].str[:4].astype(int)
        monthly_totals["MONTH"] = monthly_totals["YEAR_MONTH"].str[5:7].astype(int)

        # Create previous year dataframe
        prev_year_df = monthly_totals[["YEAR", "MONTH", "EXPENSE_AMOUNT"]].copy()
        prev_year_df["YEAR"] += 1  # shift year forward so we can match later
        prev_year_df.rename(columns={"EXPENSE_AMOUNT": "EXPENSE_AMOUNT_LAST_YEAR"}, inplace=True)


        # Merge back with current data
        monthly_totals = monthly_totals.merge(
            prev_year_df,
            on=["YEAR", "MONTH"],
            how="left"
        )


        # Calculate Year-over-Year % Change
        monthly_totals["YoY_CHANGE"] = (
            (monthly_totals["EXPENSE_AMOUNT"] - monthly_totals["EXPENSE_AMOUNT_LAST_YEAR"])
            / monthly_totals["EXPENSE_AMOUNT_LAST_YEAR"]
        ) * 100

        monthly_totals["YoY_CHANGE"] = monthly_totals["YoY_CHANGE"].round(1)

        
        # Calculate Year-to-Date (YtD) Change
        dec_totals = monthly_totals[monthly_totals["MONTH"] == 12][["YEAR", "EXPENSE_AMOUNT"]].copy()
        dec_totals.columns = ["YEAR_DEC", "DEC_EXPENSE"]
        dec_totals["YEAR_DEC"] += 1  # so 2024 Dec becomes 2025 reference

        # Merge back with current data
        monthly_totals = monthly_totals.merge(
            dec_totals,
            left_on="YEAR",
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
        
        # Number of months selection on chart (min 6, max 36)
        chart_slider = st.slider("Months Selection", min_value=6, max_value=36, value=13, step=1)
        
        monthly_totals_filtered = (
            monthly_totals.sort_values("YEAR_MONTH")
            .tail(chart_slider)
            .copy()
        )

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
                x=alt.X("YEAR_MONTH:N", title="Month", sort=None, axis=alt.Axis(labelAngle=-40)),
                y=alt.Y(
                    "EXPENSE_AMOUNT:Q",
                    title="Total Expense",
                    scale=alt.Scale(domain=[0, rounded_max]),
                    axis=alt.Axis(labelFontSize=10, titleFontSize=12)
                ),
                color=alt.Color("BAR_COLOR:N", scale=None),  # use predefined color, no gradient
                tooltip=[
                    alt.Tooltip("YEAR_MONTH", title="Month"),
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
                x="YEAR_MONTH:N",
                y="12M_MA:Q"
            )
            
            labels = alt.Chart(monthly_totals_filtered).mark_text(
                dy=-15,  # move label above bar
                fontSize=13,
                color="black"
            ).encode(
                x=alt.X("YEAR_MONTH:N", title="Month", sort=None, axis=alt.Axis(labelAngle=-40)),
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
                x="YEAR_MONTH:N",
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

            st.divider()

# **************************************************************** DETAILED BREAKDOWN CHART AND TABLE - START **************************************************************** #

            # For Detailed Breakdown chart
            selected_period = st.selectbox("Select a Month for Detailed Breakdown", options=monthly_totals_filtered["YEAR_MONTH"].tolist(), index=len(monthly_totals_filtered) - 1)  # latest month selected by default

            conn = obj.get_db_connection()
            #cursor = conn.cursor()
            sql_query = f"""SELECT * FROM REPORTABLE_EXPENSES WHERE 1=1 AND EXPENSE_PERIOD = '{selected_period}'"""
            
            df_group_breakdown = pd.read_sql_query(sql_query, conn)
            conn.close()

            df_group_breakdown["EXPENSE_AMOUNT"] = (
                df_group_breakdown["EXPENSE_AMOUNT"]
                .astype(str)
                .str.replace(",", ".", regex=False) # This is for number format (comma or dot)
                .astype(float)
            )

            # Group and sum
            group_summary = (
                df_group_breakdown
                .groupby("EXPENSE_GROUP")["EXPENSE_AMOUNT"]
                .sum()
                .reset_index()
                .sort_values("EXPENSE_AMOUNT", ascending=False)
            )


            st.markdown(f"### 📊 Expense Breakdown for {selected_period}")



            # Total sum for percentage calculation
            total_expense = group_summary["EXPENSE_AMOUNT"].sum()
            group_summary["PERCENT"] = (group_summary["EXPENSE_AMOUNT"] / total_expense * 100).round(1)

            # Altair Pie Chart
            pie_chart = alt.Chart(group_summary).mark_arc(innerRadius=50).encode(
                theta=alt.Theta("EXPENSE_AMOUNT:Q", title=""),
                color=alt.Color("EXPENSE_GROUP:N", legend=alt.Legend(title="Expense Group")),
                tooltip=[
                    alt.Tooltip("EXPENSE_GROUP:N", title="Group"),
                    alt.Tooltip("EXPENSE_AMOUNT:Q", format=",.0f", title="Amount"),
                    alt.Tooltip("PERCENT:Q", format=".1f", title="% of Total")
                ]
            ).properties(
                width=400,
                height=400,
                title=f"Expense Group Distribution – {selected_period}"
            )


            # Actually there are sub columns :)
            col1, col2 = st.columns([1, 1])

            with col1:
                st.altair_chart(pie_chart, use_container_width=True)

            with col2:
                st.dataframe(group_summary[["EXPENSE_GROUP", "EXPENSE_AMOUNT", "PERCENT"]], hide_index=True)


# **************************************************************** DETAILED BREAKDOWN CHART AND TABLE - END **************************************************************** #


# **************************************************************** TABLE DATA OF CHART - START **************************************************************** #

        # ---- Table ----
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
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

# **************************************************************** TABLE DATA OF CHART - END **************************************************************** #

            st.divider()

# **************************************************************** FUTURE EXPENSES TABLE - START **************************************************************** #

            # Future Expsense (Installments) Summary
            conn = obj.get_db_connection()
            #cursor = conn.cursor()
            sql_query = ("SELECT * FROM REPORTABLE_EXPENSES WHERE 1=1 AND FUTURE_EXPENSE = 1")
            
            df_future_expenses = pd.read_sql_query(sql_query, conn)
            conn.close()

            df_future_expenses["EXPENSE_AMOUNT"] = (
                df_future_expenses["EXPENSE_AMOUNT"]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .astype(float)
            )

            # Group and sum
            future_expenses = (
                df_future_expenses
                .groupby("EXPENSE_PERIOD")["EXPENSE_AMOUNT"]
                .sum()
                .reset_index()
                .sort_values("EXPENSE_PERIOD", ascending=True)
            )

            # Renaming columns
            future_expenses.rename(columns={
                "EXPENSE_PERIOD": "Period",
                "EXPENSE_AMOUNT":"Expense Amount"
                }, inplace=True)

            if len(future_expenses) > 0:
                st.markdown(f"### 📊 Future Expenses")
                st.dataframe(future_expenses, use_container_width=True, hide_index=True)
            else:
                st.markdown("**There is no future dated expense.**")


# **************************************************************** FUTURE EXPENSES TABLE - END **************************************************************** #

            st.divider()

# **************************************************************** REMINDER TABLE - START **************************************************************** #

            st.subheader("🔍 View & Filter Reminders")

            all_reminders = obj.get_all_reminders()
            df = pd.DataFrame(all_reminders)

            if not df.empty:
                # Convert date columns
                df["REMINDER_DATE"] = pd.to_datetime(df["REMINDER_DATE"], errors="coerce")
                df["DONE_DATE"] = pd.to_datetime(df["DONE_DATE"], errors="coerce")

                # Filters
                today = pd.to_datetime(date.today())
                filter_option = st.radio(
                    "Show:",
                    ["All", "Upcoming", "Overdue", "Done", "Active"],
                    horizontal=True
                )

                if filter_option == "Upcoming":
                    df = df[(df["REMINDER_DATE"] >= today) & (df["IS_DONE"] == 0)]
                elif filter_option == "Overdue":
                    df = df[(df["REMINDER_DATE"] < today) & (df["IS_DONE"] == 0)]
                elif filter_option == "Done":
                    df = df[df["IS_DONE"] == 1]
                elif filter_option == "Active":
                    df = df[df["IS_ACTIVE"] == 1]

                # Format date columns
                df["REMINDER_DATE"] = df["REMINDER_DATE"].dt.strftime("%Y-%m-%d")
                df["DONE_DATE"] = df["DONE_DATE"].dt.strftime("%Y-%m-%d")

                # Drop unwanted columns
                df_display = df.drop(columns=["CREATED_AT", "UPDATED_AT", "IS_ACTIVE", "IS_DONE"])

                # Show the table
                st.dataframe(df_display, use_container_width=True, hide_index=True)


                # User selects a reminder from the list by ID
                st.markdown("### ⚙️ Manage Reminder")

                selected_row = st.selectbox("Select a reminder", df["REMINDER_NAME"] + " — " + df["REMINDER_DATE"], index=0)
                selected_id = df[df["REMINDER_NAME"] + " — " + df["REMINDER_DATE"] == selected_row]["ID"].iloc[0]
                st.write("Selected ID:", selected_id)
                #st.write("type of selected_id ", type(selected_id))

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✅ Mark as Done"):
                        success = obj.mark_reminder_done(selected_id)
                        

                        print("success >> ", success)
                        st.write("Success:", success)

                        conn = obj.get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT IS_DONE FROM TBL_REMINDERS WHERE ID = ?", (selected_id,))
                        print("Post-update IS_DONE value:", cursor.fetchone())
                        conn.close()


                        if success:
                            st.success("Marked as done.")
                            time.sleep(3)
                            st.rerun()
                        else:
                            st.error("Failed to update reminder.")

                with col2:
                    if st.button("🗑️ Delete Reminder"):
                        success = obj.soft_delete_reminder(selected_id)
                        if success:
                            st.success("Reminder deleted (soft delete).")
                            st.rerun()
                        else:
                            st.error("Failed to delete reminder.")


            else:
                st.info("No reminders to show.")
# **************************************************************** REMINDER TABLE - END **************************************************************** #



def show(navigate_to):
    st.title("Dashboard")

    display_menu_buttons(navigate_to)

    show_page_contents()









