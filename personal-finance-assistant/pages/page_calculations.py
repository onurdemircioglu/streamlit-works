import streamlit as st
import pandas as pd
from datetime import date
from utils.utils import display_menu_buttons
from utils import my_functions

obj = my_functions.MyClass()


import streamlit as st
import pandas as pd

from datetime import date

# --- Calculation logic ---
def calculate_loan_schedule_with_fees(principal, monthly_interest_percent, term_months, extra_fees=0.0):
    r = monthly_interest_percent / 100
    tax_rate = 0.30  # 15% KKDF + 15% BSMV

    # Monthly fixed payment (based on full loan, not what you actually receive)
    A = principal * (r * (1 + r)**term_months) / ((1 + r)**term_months - 1)

    schedule = []
    remaining_principal = principal
    total_interest_with_tax = 0

    for month in range(1, term_months + 1):
        interest = remaining_principal * r
        tax = interest * tax_rate
        interest_with_tax = interest + tax
        principal_payment = A - interest_with_tax
        remaining_principal -= principal_payment
        total_interest_with_tax += interest_with_tax

        schedule.append({
            "Month": month,
            "Monthly Payment": round(A, 2),
            "Principal": round(principal_payment, 2),
            "Interest": round(interest, 2),
            "KKDF+BSMV": round(tax, 2),
            "Remaining Principal": round(max(remaining_principal, 0), 2)
        })

    effective_amount = principal - extra_fees
    return schedule, round(A, 2), round(total_interest_with_tax, 2), round(effective_amount, 2)



def calculate_npv(initial_investment, discount_rate, cash_flows):
    npv = -initial_investment  # Initial investment is negative cash flow
    for t, cash in enumerate(cash_flows, start=1):
        npv += cash / ((1 + discount_rate) ** t)
    return round(npv, 2)




def calculation_tabs():
    st.title("🧮 Financial Calculations")

    tabs = st.tabs(["💸 Loan Calculator", "📈 Compound Interest", "📉 Net Present Value", "💰 Future Value"])

    with tabs[0]:
        col1, col2 = st.columns(2)

        with col1:
            st.header("Loan Calculator")
            # Add loan inputs & results here

            loan_amount = st.number_input("Total loan amount", min_value=1, step=100, key="loan_amount")
            loan_term = st.slider("Term (months)", min_value=3, max_value=120, step=1, key="loan_term")

            # Display duration label
            if loan_term:
                if loan_term < 12:
                    st.write(f"Loan term: {loan_term} months")
                else:
                    years = loan_term // 12
                    months = loan_term % 12
                    if years > 1:
                        if months > 1:
                            duration_text = f"{years} years" + (f" {months} months" if months > 0 else "")
                        else:
                            duration_text = f"{years} years" + (f" {months} month" if months > 0 else "")
                    else:
                        if months > 1:
                            duration_text = f"{years} year" + (f" {months} months" if months > 0 else "")
                        else:
                            duration_text = f"{years} year" + (f" {months} month" if months > 0 else "")


                    st.write(f"Loan term: {duration_text}")
                        
            loan_interest = st.number_input("Interest rate (%)", min_value=0.01, step=0.01, key="loan_interest")
            extra_fees = st.number_input("Upfront costs (fees + insurance)", min_value=0.0, value=1287.50)

            # Calculate
            if st.button("Calculate"):
    
                schedule, monthly_payment, total_tax, net_disbursed = calculate_loan_schedule_with_fees(
                    loan_amount, loan_interest, loan_term, extra_fees=extra_fees
                )


                st.success(f"Monthly Installment: ₺{monthly_payment:,.2f}")
                st.info(f"Effective cash received: ₺{net_disbursed:,.2f}")

                # Table
                df_schedule = pd.DataFrame(schedule)
                st.dataframe(df_schedule, use_container_width=True)



# The bank uses a declining balance interest model with monthly compounding interest


    with tabs[1]:
        st.header("Compound Interest Calculator")
        # Inputs: principal, rate, time, compounding frequency

    with tabs[2]:
        st.header("Net Present Value (NPV)")
        # Inputs: cash flows, discount rate

        initial_investment = st.number_input("Initial Investment", value=10000.0, step=100.0)
        discount_rate = st.number_input("Discount Rate (%)", value=10.0, step=0.1) / 100
        periods = st.number_input("Number of Periods (Years)", min_value=1, max_value=20, step=1)

        cash_flows = []
        for i in range(1, int(periods) + 1):
            cash = st.number_input(f"Cash Flow at Year {i}", value=2000.0, step=100.0, key=f"cf_{i}")
            cash_flows.append(cash)

        if st.button("💰 Calculate NPV"):
            npv_result = calculate_npv(initial_investment, discount_rate, cash_flows)
            st.success(f"📌 Net Present Value (NPV): {npv_result:,.2f} TL")

    with tabs[3]:
        st.header("Future Value")
        # Inputs: periodic contribution, interest rate, number of periods


def show(navigate_to):
    st.title("Latest Entries")

    display_menu_buttons(navigate_to)

    calculation_tabs()



