import streamlit as st
import pandas as pd
from datetime import date
from utils.utils import display_menu_buttons
from utils import my_functions


#obj = my_functions.MyClass()




# **************************************************************** REMINDER TABLE - START **************************************************************** #
import pandas as pd

def calculate_loan_schedule(
    loan_amount=50000,
    months=12,
    annual_interest_rate=5.49,
    kkdf_rate=0.15,
    bsmv_rate=0.15
):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    effective_rate = monthly_interest_rate * (1 + kkdf_rate + bsmv_rate)

    # Calculate monthly installment using effective interest
    pmt = loan_amount * effective_rate * (1 + effective_rate)**months / ((1 + effective_rate)**months - 1)
    pmt = round(pmt, 2)

    schedule = []
    remaining = loan_amount

    for i in range(1, months + 1):
        interest = round(remaining * monthly_interest_rate, 2)
        kkdf = round(interest * kkdf_rate, 2)
        bsmv = round(interest * bsmv_rate, 2)
        principal = round(pmt - interest - kkdf - bsmv, 2)
        remaining = round(remaining - principal, 2)

        schedule.append({
            "Installment No": i,
            "Installment Amount (Taksit)": pmt,
            "Principal (Anapara)": principal,
            "Interest (Faiz)": interest,
            "KKDF (15%)": kkdf,
            "BSMV (15%)": bsmv,
            "Remaining Principal": max(remaining, 0)
        })

    df = pd.DataFrame(schedule)
    return pmt, df

""" # Example usage:
monthly_payment, table = calculate_loan_schedule()
print(f"Monthly payment: {monthly_payment} TL\n")
print(table.to_string(index=False)) """


# **************************************************************** REMINDER TABLE - END **************************************************************** #

def show(navigate_to):

    st.title("I am Test Page, leave this page immediately")

    display_menu_buttons(navigate_to)

    #show_page_contents()


