# pages/3_Statistics.py
import streamlit as st
import pandas as pd
import altair as alt
from utils.db import fetch_all_ratings

st.title("📈 Statistics & Analytics")

# --- Fetch data ---
rows = fetch_all_ratings()
if not rows:
    st.info("No ratings found. Please add some first.")
    st.stop()

df = pd.DataFrame(rows, columns=rows[0].keys())
df["DATE"] = pd.to_datetime(df["DATE"])
df["AVG_SCORE"] = df[["TASTE", "PRICE"]].sum(axis=1)

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
    (filtered_df["DATE"] >= pd.to_datetime(start_date)) &
    (filtered_df["DATE"] <= pd.to_datetime(end_date))
]

# --- Metrics ---
st.subheader("Overall Metrics")
total_ratings = len(filtered_df)
st.metric("Total Ratings", total_ratings)

# --- Count of ratings per month, per store, per category ---
st.subheader("Ratings Count")
col1, col2, col3 = st.columns(3)

# Per Month
monthly_count = filtered_df.groupby(filtered_df["DATE"].dt.to_period("M")).size().reset_index(name="COUNT")
col1.altair_chart(
    alt.Chart(monthly_count).mark_bar().encode(
        x="DATE:T",
        y="COUNT:Q",
        tooltip=["DATE", "COUNT"]
    ),
    use_container_width=True
)

# Per Store
store_count = filtered_df.groupby("STORE_NAME").size().reset_index(name="COUNT")
col2.altair_chart(
    alt.Chart(store_count).mark_bar().encode(
        x=alt.X("STORE_NAME", sort="-y"),
        y="COUNT:Q",
        tooltip=["STORE_NAME", "COUNT"]
    ),
    use_container_width=True
)

# Per Category
category_count = filtered_df.groupby("CATEGORY").size().reset_index(name="COUNT")
col3.altair_chart(
    alt.Chart(category_count).mark_bar().encode(
        x=alt.X("CATEGORY", sort="-y"),
        y="COUNT:Q",
        tooltip=["CATEGORY", "COUNT"]
    ),
    use_container_width=True
)

# --- Top-rated stores/categories ---
st.subheader("Top-rated Stores/Categories")
agg_store = filtered_df.groupby("STORE_NAME")["AVG_SCORE"].mean().reset_index().sort_values("AVG_SCORE", ascending=False)
agg_category = filtered_df.groupby("CATEGORY")["AVG_SCORE"].mean().reset_index().sort_values("AVG_SCORE", ascending=False)

col1, col2 = st.columns(2)
col1.altair_chart(
    alt.Chart(agg_store.head(10)).mark_bar().encode(
        x=alt.X("STORE_NAME", sort="-y"),
        y="AVG_SCORE:Q",
        tooltip=["STORE_NAME", "AVG_SCORE"]
    ),
    use_container_width=True
)
col2.altair_chart(
    alt.Chart(agg_category.head(10)).mark_bar().encode(
        x=alt.X("CATEGORY", sort="-y"),
        y="AVG_SCORE:Q",
        tooltip=["CATEGORY", "AVG_SCORE"]
    ),
    use_container_width=True
)

# --- Compare stores or categories side by side ---
st.subheader("Store/Category Comparison")
compare_option = st.radio("Compare by:", ["Store", "Category"])

if compare_option == "Store":
    comp_df = filtered_df.groupby("STORE_NAME")[["TASTE", "PRICE", "AVG_SCORE"]].mean().reset_index()
    x_field = "STORE_NAME"
else:
    comp_df = filtered_df.groupby("CATEGORY")[["TASTE", "PRICE", "AVG_SCORE"]].mean().reset_index()
    x_field = "CATEGORY"


# Ensure numeric types for Altair
for col in ["TASTE", "PRICE", "AVG_SCORE"]:
    comp_df[col] = comp_df[col].astype(float)



# Create the bar chart using transform_fold
comp_chart = alt.Chart(comp_df).transform_fold(
    ["TASTE", "PRICE", "AVG_SCORE"],
    as_=["key", "value"]
).mark_bar().encode(
    x=alt.X(f"{x_field}:N", sort="-y"),
    y=alt.Y("value:Q"),
    color=alt.Color("key:N"),
    tooltip=[alt.Tooltip(f"{x_field}:N"), alt.Tooltip("key:N"), alt.Tooltip("value:Q", format=".2f")]
)

st.altair_chart(comp_chart, use_container_width=True)



# --- Heatmap of taste vs price per category ---
st.subheader("Taste vs Price Heatmap by Category")
heat_df = filtered_df.groupby(["CATEGORY", "TASTE", "PRICE"]).size().reset_index(name="COUNT")
heatmap = alt.Chart(heat_df).mark_rect().encode(
    x="TASTE:O",
    y="PRICE:O",
    color="COUNT:Q",
    tooltip=["CATEGORY", "TASTE", "PRICE", "COUNT"]
).facet(
    column="CATEGORY:N"
)
st.altair_chart(heatmap, use_container_width=True)



# --- Trend Analysis Section ---
st.subheader("📊 Trend Analysis per Food")

# Dropdowns to select store, category, and food
stores = ["All"] + sorted(df["STORE_NAME"].unique().tolist())
categories = ["All"] + sorted(df["CATEGORY"].unique().tolist())
foods = ["All"] + sorted(df["FOOD_NAME"].unique().tolist())

trend_store = st.selectbox("Store", stores, key="trend_store")
trend_category = st.selectbox("Category", categories, key="trend_category")
trend_food = st.selectbox("Food Name", foods, key="trend_food")

# Date range filter
start_date = st.date_input("Start Date", value=df["DATE"].min(), key="trend_start")
end_date = st.date_input("End Date", value=df["DATE"].max(), key="trend_end")

# Moving average window
window_days = st.slider("Moving Average Window (days)", min_value=1, max_value=30, value=7)

# Apply filters
trend_df = df.copy()
if trend_store != "All":
    trend_df = trend_df[trend_df["STORE_NAME"] == trend_store]
if trend_category != "All":
    trend_df = trend_df[trend_df["CATEGORY"] == trend_category]
if trend_food != "All":
    trend_df = trend_df[trend_df["FOOD_NAME"] == trend_food]
trend_df = trend_df[
    (trend_df["DATE"] >= pd.to_datetime(start_date)) &
    (trend_df["DATE"] <= pd.to_datetime(end_date))
]

if trend_df.empty:
    st.info("No data for selected filters.")
else:
    # Compute daily average score
    trend_df["AVG_SCORE"] = trend_df[["TASTE", "PRICE"]].sum(axis=1)
    daily_avg = trend_df.groupby("DATE")["AVG_SCORE"].mean().reset_index()
    daily_avg = daily_avg.sort_values("DATE")
    
    # Compute moving average
    daily_avg["MOVING_AVG"] = daily_avg["AVG_SCORE"].rolling(window=window_days, min_periods=1).mean()
    
    # Plot line chart
    import altair as alt
    line_chart = alt.Chart(daily_avg).mark_line(point=True).encode(
        x=alt.X("DATE:T", title="Date"),
        y=alt.Y("AVG_SCORE:Q", title="Average Score"),
        tooltip=[alt.Tooltip("DATE:T", title="Date"),
                 alt.Tooltip("AVG_SCORE:Q", title="Daily Avg", format=".2f"),
                 alt.Tooltip("MOVING_AVG:Q", title=f"{window_days}-day Moving Avg", format=".2f")]
    )
    
    moving_avg_line = alt.Chart(daily_avg).mark_line(color="red").encode(
        x="DATE:T",
        y="MOVING_AVG:Q"
    )
    
    st.altair_chart(line_chart + moving_avg_line, use_container_width=True)




# --- Category Comparisons ---
st.subheader("📊 Category Comparisons")

# Filters
category_store_options = ["All"] + sorted(df["STORE_NAME"].unique().tolist())
selected_store_cat = st.selectbox("Filter by Store (optional)", category_store_options)

# Apply store filter if selected
cat_df = df.copy()
if selected_store_cat != "All":
    cat_df = cat_df[cat_df["STORE_NAME"] == selected_store_cat]

# Compute average score
cat_df["AVG_SCORE"] = cat_df[["TASTE", "PRICE"]].sum(axis=1)

# --- 1. Category trend over months ---
cat_df["MONTH"] = cat_df["DATE"].dt.to_period("M").dt.to_timestamp()
monthly_avg = cat_df.groupby(["MONTH", "CATEGORY"])["AVG_SCORE"].mean().reset_index()

import altair as alt

line_chart = alt.Chart(monthly_avg).mark_line(point=True).encode(
    x=alt.X("MONTH:T", title="Month"),
    y=alt.Y("AVG_SCORE:Q", title="Average Score"),
    color=alt.Color("CATEGORY:N"),
    tooltip=[alt.Tooltip("MONTH:T", title="Month"),
             alt.Tooltip("CATEGORY:N"),
             alt.Tooltip("AVG_SCORE:Q", title="Avg Score", format=".2f")]
).properties(height=300)

st.altair_chart(line_chart, use_container_width=True)

# --- 2. Category comparison across stores ---
store_cat_avg = cat_df.groupby(["STORE_NAME", "CATEGORY"])["AVG_SCORE"].mean().reset_index()

bar_chart = alt.Chart(store_cat_avg).mark_bar().encode(
    x=alt.X("STORE_NAME:N", title="Store", sort="-y"),
    y=alt.Y("AVG_SCORE:Q", title="Average Score"),
    color=alt.Color("CATEGORY:N"),
    tooltip=[alt.Tooltip("STORE_NAME:N"), alt.Tooltip("CATEGORY:N"), alt.Tooltip("AVG_SCORE:Q", format=".2f")]
).properties(height=300)

st.altair_chart(bar_chart, use_container_width=True)
