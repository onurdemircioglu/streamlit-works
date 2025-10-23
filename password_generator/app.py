import streamlit as st
import string
import random


MAX_PASSWORD_LENGTH = 32

# Page setup
st.set_page_config(
    page_title="Password Generator",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Header
st.title("🔐 Password Generator")
st.write("Create a strong password")


# About
with st.expander("About", expanded=False):
    st.markdown(
        """
        I was inspired by this: [RPA Sample Password Generator](https://www.rpasamples.com/passwordgenerator)
        """
    )

# Password Generator function
def generate_passwords(count, length, min_upper, min_lower, min_num, min_sym):
    chars = {
        "upper": string.ascii_uppercase,
        "lower": string.ascii_lowercase,
        "num": string.digits,
        "sym": string.punctuation
    }

    passwords = []
    for _ in range(count):
        password_chars = []
        password_chars += random.choices(chars["upper"], k=min_upper)
        password_chars += random.choices(chars["lower"], k=min_lower)
        password_chars += random.choices(chars["num"], k=min_num)
        password_chars += random.choices(chars["sym"], k=min_sym)

        remaining = length - len(password_chars)
        combined = "".join([
            chars["upper"] if min_upper else "",
            chars["lower"] if min_lower else "",
            chars["num"] if min_num else "",
            chars["sym"] if min_sym else "",
        ])
        password_chars += random.choices(combined, k=remaining)
        random.shuffle(password_chars)
        passwords.append("".join(password_chars))
    return passwords

with st.container():
    # col_parameters, col_results = st.columns([1, 1])
    col_parameters, col_results = st.columns(2)

    with col_parameters:
        length_selection = st.slider("Choose length", min_value=8, max_value=MAX_PASSWORD_LENGTH, step=1)
        count_selection = st.slider("How many password do you want to create?", min_value=1, max_value=10)
        
        # Parameter section
        col_1, col_2, col_3, col_4 = st.columns(4)
        with col_1:
            uppercase_selection = st.checkbox("Upper case",)
        with col_2:
            lowercase_selection = st.checkbox("Lower case")
        with col_3:
            numbers_selection = st.checkbox("Numbers")
        with col_4:
            symbols_selection = st.checkbox("Symbols")
        
        # Parameter values
        col_5, col_6, col_7, col_8 = st.columns(4)
        with col_5:
            uppercase_min_selection = st.number_input("Min Upper case",min_value=1,max_value=MAX_PASSWORD_LENGTH)
        with col_6:
            lowercase_min_selection = st.number_input("Min Lower case",min_value=1,max_value=MAX_PASSWORD_LENGTH)
        with col_7:
            numbers_min_selection = st.number_input("Min Number count",min_value=1,max_value=MAX_PASSWORD_LENGTH)
        with col_8:
            symbols_min_selection = st.number_input("Min symbols count",min_value=1,max_value=MAX_PASSWORD_LENGTH)
        
    create_password = st.button("Create Passwords")

    # If the parameters are not selected set parameter values to zero.
    if not uppercase_selection:
        uppercase_min_selection = 0
    
    if not lowercase_selection:
        lowercase_min_selection = 0
    
    if not numbers_selection:
        numbers_min_selection = 0
    
    if not symbols_selection:
        symbols_min_selection = 0

    # Create password action
    if create_password:
        if not any ([uppercase_selection, lowercase_selection, numbers_selection, symbols_selection]):
            st.write("Please select at least one option")
        elif int(uppercase_min_selection) + int(lowercase_min_selection) + int(numbers_min_selection) + int(symbols_min_selection) > MAX_PASSWORD_LENGTH:
            st.write("Sum of minimum counts exceeds chosen length")
        else:
            with col_results:
                result = generate_passwords(
                    count_selection,
                    length_selection,
                    uppercase_min_selection,
                    lowercase_min_selection,
                    numbers_min_selection,
                    symbols_min_selection
                )
                st.write(result)