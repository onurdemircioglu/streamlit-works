# pages/2_View_Ratings.py
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from utils.db import fetch_all_ratings

st.title("📊 View Food Ratings")

# --- Fetch data ---
rows = fetch_all_ratings()
if not rows:
    st.info("No ratings found. Please add some first.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(rows, columns=rows[0].keys())

# --- Filters ---
with st.expander("Filters"):
    stores = ["All"] + sorted(df["STORE_NAME"].unique().tolist())
    categories = ["All"] + sorted(df["CATEGORY"].unique().tolist())

    selected_store = st.selectbox("Store", stores)
    selected_category = st.selectbox("Category", categories)
    start_date = st.date_input("Start Date", value=df["DATE"].min())
    end_date = st.date_input("End Date", value=df["DATE"].max())

# Apply filters
filtered_df = df.copy()
if selected_store != "All":
    filtered_df = filtered_df[filtered_df["STORE_NAME"] == selected_store]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["CATEGORY"] == selected_category]
filtered_df = filtered_df[
    (pd.to_datetime(filtered_df["DATE"]) >= pd.to_datetime(start_date)) &
    (pd.to_datetime(filtered_df["DATE"]) <= pd.to_datetime(end_date))
]

# --- Display table ---
st.subheader(f"Showing {len(filtered_df)} ratings")
st.dataframe(filtered_df.reset_index(drop=True))

# --- Average ratings ---
st.subheader("Average Ratings")
if not filtered_df.empty:
    avg_taste = filtered_df["TASTE"].mean()
    avg_price = filtered_df["PRICE"].mean()
    avg_score = filtered_df[["TASTE", "PRICE"]].sum(axis=1).mean()
    st.metric("Average Taste", f"{avg_taste:.2f}")
    st.metric("Average Price", f"{avg_price:.2f}")
    st.metric("Average Score", f"{avg_score:.2f}")

# --- Chart selection ---
chart_type = st.selectbox(
    "Select Chart Type",
    ["Bar Chart: Top-rated Foods", "Scatter Plot: Taste vs Price", "Monthly Trend (Avg Score)"]
)

if filtered_df.empty:
    st.warning("No data for chart.")
else:
    if chart_type == "Bar Chart: Top-rated Foods":
        # Calculate average score per food using sum of taste + price
        filtered_df["AVG_SCORE"] = filtered_df[["TASTE", "PRICE"]].sum(axis=1)  # This line has been changed
        top_foods = filtered_df.groupby("FOOD_NAME")["AVG_SCORE"].mean().reset_index()
        top_foods = top_foods.sort_values("AVG_SCORE", ascending=False).head(10)

        bar = alt.Chart(top_foods).mark_bar().encode(
            x=alt.X("FOOD_NAME", sort="-y", title="Food"),
            y=alt.Y("AVG_SCORE", title="Average Score"),
            tooltip=["FOOD_NAME", "AVG_SCORE"]
        )
        st.altair_chart(bar, use_container_width=True)

    elif chart_type == "Scatter Plot: Taste vs Price":
        # Add Average Score column
        filtered_df["AVG_SCORE"] = filtered_df[["TASTE", "PRICE"]].sum(axis=1)

        # Toggle for aggregation
        agg_option = st.radio(
            "View Mode",
            ["Individual Ratings", "Aggregated by Store", "Aggregated by Category"],
            horizontal=True
        )

        if agg_option == "Aggregated by Store":
            # Aggregate by store
            agg_df = (
                filtered_df.groupby(["STORE_NAME", "CATEGORY"])
                .agg({
                    "TASTE": "mean",
                    "PRICE": "mean",
                    "AVG_SCORE": "mean",
                    "FOOD_NAME": "count"  # Count of ratings per store
                })
                .rename(columns={"FOOD_NAME": "NUM_RATINGS"})
                .reset_index()
            )

            scatter = alt.Chart(agg_df).mark_circle().encode(
                x=alt.X("PRICE", title="Average Price"),
                y=alt.Y("TASTE", title="Average Taste"),
                color="CATEGORY",
                size=alt.Size("NUM_RATINGS", title="Number of Ratings"),  # This line has been added
                tooltip=["STORE_NAME", "CATEGORY", "TASTE", "PRICE", "AVG_SCORE", "NUM_RATINGS"]  # This line updated
            )
            st.altair_chart(scatter, use_container_width=True)


        elif agg_option == "Aggregated by Category":
            # Aggregate by category
            agg_df = (
                filtered_df.groupby("CATEGORY")
                .agg({
                    "TASTE": "mean",
                    "PRICE": "mean",
                    "AVG_SCORE": "mean",
                    "FOOD_NAME": "count"  # Count of ratings per category
                })
                .rename(columns={"FOOD_NAME": "NUM_RATINGS"})
                .reset_index()
            )

            scatter = alt.Chart(agg_df).mark_circle().encode(
                x=alt.X("PRICE", title="Average Price"),
                y=alt.Y("TASTE", title="Average Taste"),
                color="CATEGORY",
                size=alt.Size("NUM_RATINGS", title="Number of Ratings"),  # This line has been added
                tooltip=["CATEGORY", "TASTE", "PRICE", "AVG_SCORE", "NUM_RATINGS"]  # This line updated
            )
            st.altair_chart(scatter, use_container_width=True)


        else:  # Individual Ratings
            scatter = alt.Chart(filtered_df).mark_circle(size=100).encode(
                x=alt.X("PRICE", title="Price"),
                y=alt.Y("TASTE", title="Taste"),
                color="CATEGORY",
                tooltip=["FOOD_NAME", "STORE_NAME", "TASTE", "PRICE", "AVG_SCORE"]
            )
            st.altair_chart(scatter, use_container_width=True)



    elif chart_type == "Monthly Trend (Avg Score)":
        filtered_df["DATE"] = pd.to_datetime(filtered_df["DATE"])
        filtered_df["YEAR_MONTH"] = filtered_df["DATE"].dt.to_period("M").astype(str)
        filtered_df["AVG_SCORE"] = filtered_df[["TASTE", "PRICE"]].sum(axis=1)
        monthly = filtered_df.groupby("YEAR_MONTH")["AVG_SCORE"].mean().reset_index()

        line = alt.Chart(monthly).mark_line(point=True).encode(
            x=alt.X("YEAR_MONTH", title="Month"),
            y=alt.Y("AVG_SCORE", title="Average Score"),
            tooltip=["YEAR_MONTH", "AVG_SCORE"]
        )
        st.altair_chart(line, use_container_width=True)
