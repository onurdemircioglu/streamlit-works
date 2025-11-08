# pages/1_Add_Rating.py
import streamlit as st
from datetime import date
from utils.db import insert_rating, init_db, get_lookup_values, insert_lookup_value

init_db()
st.title("🍽️ Add Food Rating")

# --- Initialize session state ---
if "categories" not in st.session_state:
    st.session_state["categories"] = get_lookup_values("LOOKUP_CATEGORIES")  # This line has been added or changed
if "stores" not in st.session_state:
    st.session_state["stores"] = get_lookup_values("LOOKUP_STORES")  # This line has been added or changed

# --- Expander to add new store/category ---
with st.expander("Add new store or category"):
    new_store = st.text_input("New store name")
    if st.button("Add Store"):
        if new_store.strip():
            insert_lookup_value("LOOKUP_STORES", new_store.strip())
            st.session_state["stores"] = get_lookup_values("LOOKUP_STORES")  # This line has been added or changed
            st.success("Store added.")
        else:
            st.warning("Please enter a valid store name.")

    new_category = st.text_input("New category name")
    if st.button("Add Category"):
        if new_category.strip():
            insert_lookup_value("LOOKUP_CATEGORIES", new_category.strip())
            st.session_state["categories"] = get_lookup_values("LOOKUP_CATEGORIES")  # This line has been added or changed
            st.success("Category added.")
        else:
            st.warning("Please enter a valid category name.")

# --- Input Form ---
with st.form("add_rating_form"):
    col1, col2 = st.columns(2)

    with col1:
        selected_date = st.date_input("Date", value=date.today())
        store_name = st.selectbox("Store", st.session_state["stores"])  # This line has been added or changed
        category = st.selectbox("Category", st.session_state["categories"])  # This line has been added or changed

    with col2:
        food_name = st.text_input("Food Name")
        taste = st.slider("Taste Rating (1–5)", 1.0, 5.0, 3.0, 0.5)
        price = st.slider("Price Rating (1–5)", 1.0, 5.0, 3.0, 0.5)

    comments = st.text_area("Comments (optional)")
    submitted = st.form_submit_button("Submit Rating")

# --- Submission Logic ---
if submitted:
    insert_rating(str(selected_date), store_name, food_name, category, taste, price, comments)
    st.success("✅ Rating added successfully!")
