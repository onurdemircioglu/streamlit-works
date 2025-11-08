# pages/4_Insights.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.db import fetch_all_ratings

st.title("💡 Insights")

# --- Fetch data ---
rows = fetch_all_ratings()
if not rows:
    st.info("No ratings found. Please add some first.")
    st.stop()

df = pd.DataFrame(rows, columns=rows[0].keys())
df["DATE"] = pd.to_datetime(df["DATE"])

# --- User inputs ---
st.subheader("Unrated Foods")
months = st.number_input("Number of months without rating:", min_value=1, max_value=24, value=3)

stores = ["All"] + sorted(df["STORE_NAME"].unique().tolist())
categories = ["All"] + sorted(df["CATEGORY"].unique().tolist())
foods = ["All"] + sorted(df["FOOD_NAME"].unique().tolist())

selected_store = st.selectbox("Store", stores)
selected_category = st.selectbox("Category", categories)
selected_food = st.selectbox("Food Name", foods)

# --- Apply filters to data ---
filtered_df = df.copy()
if selected_store != "All":
    filtered_df = filtered_df[filtered_df["STORE_NAME"] == selected_store]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["CATEGORY"] == selected_category]
if selected_food != "All":
    filtered_df = filtered_df[filtered_df["FOOD_NAME"] == selected_food]

# --- Calculate threshold date ---
threshold_date = pd.Timestamp(datetime.today() - pd.DateOffset(months=months))

# --- Group by store/category/food and get last rating ---
latest_df = filtered_df.groupby(["STORE_NAME", "CATEGORY", "FOOD_NAME"])["DATE"].max().reset_index()

# --- Filter unrated foods ---
unrated_df = latest_df[latest_df["DATE"] <= threshold_date].sort_values("DATE")

st.write(f"Showing foods not rated in the last {months} month(s):")
st.dataframe(unrated_df)
