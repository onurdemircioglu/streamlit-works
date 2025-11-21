import streamlit as st
import pandas as pd
from datetime import date, datetime, timezone
from utils.utils import display_menu_buttons
from utils import my_functions
from utils.streamlit_helpers import smart_number_input
# smart_selectbox, smart_text_input, smart_text_area, smart_date_input, render_clear_button_with_confirmation

# utils_settlement.py (you can paste this at the bottom of your Streamlit file)
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Tuple

CENT = Decimal("0.01")


obj = my_functions.MyClass()


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

    tabs = st.tabs(["💸 Loan Calculator", "📈 Compound Interest", "📉 Net Present Value", "💰 Future Value", "Expense Distributor"])

    with tabs[0]:
        col1, col2 = st.columns(2)

        with col1:
            st.header("Loan Calculator")
            # Add loan inputs & results here

            loan_amount = smart_number_input("Total loan amount", min_value=1.0, step=100.0, key="key_loan_amount")
            loan_term = st.slider("Term (months)", min_value=3, max_value=120, step=1, key="key_loan_term")

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
                        
            loan_interest = smart_number_input("Interest rate (%)", min_value=0.01, step=0.01, key="key_loan_interest")
            extra_fees = smart_number_input("Upfront costs (fees + insurance)", min_value=0.0, key="key_extra_fees")

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

        initial_investment = smart_number_input("Initial Investment", min_value=0.0, step=100.0, key="key_initial_investment")
        #discount_rate = st.number_input("Discount Rate (%)", value=10.0, step=0.1) / 100
        discount_rate = smart_number_input("Discount Rate (%)", default=10.0, step=0.1, key="key_discount_rate")
        periods = st.number_input("Number of Periods (Years)", min_value=1, max_value=20, step=1, key="key_period")

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
    
    with tabs[4]:
        st.header("Expense Distributor")


        # ---------------------- State ----------------------
        if "people" not in st.session_state:
            st.session_state.people = pd.DataFrame(columns=["name"])  # only names

        if "expenses" not in st.session_state:
            # participants will be stored as a Python list of names (no ids)
            st.session_state.expenses = pd.DataFrame(
                columns=["date", "place", "amount", "payer", "participants"]
            )

        # ---------------------- Helpers ----------------------
        def normalize_name(name: str) -> str:
            return " ".join(name.split()).title()

        def fmt_money(x: float) -> str:
            try:
                return f"{float(x):,.2f}"
            except Exception:
                return str(x)

        # ---------------------- UI: People Catalog ----------------------
        #st.subheader("💸 Expense Blocks — Input")

        with st.container(border=True):
            st.subheader("People")
            st.caption("Add people once; then select them in each expense block.")

            with st.form("add_person_form", clear_on_submit=True, border=False):
                c1, c2 = st.columns([2, 1])
                person_name = c1.text_input("Person name", placeholder="e.g., Ada Lovelace")
                add_person_btn = c2.form_submit_button("Add person")
                if add_person_btn:
                    name = normalize_name(person_name)
                    if not name:
                        st.warning("Please enter a non-empty name.")
                    elif name in st.session_state.people["name"].tolist():
                        st.info(f"**{name}** already exists.")
                    else:
                        st.session_state.people = pd.concat(
                            [st.session_state.people, pd.DataFrame([{"name": name}])],
                            ignore_index=True,
                        )
                        st.success(f"Added **{name}**")

            if st.session_state.people.empty:
                st.info("No people yet — add a few above.")
            else:
                st.dataframe(
                    st.session_state.people.rename(columns={"name": "People"}),
                    use_container_width=True,
                    hide_index=True,
                )

        st.divider()

        # ---------------------- UI: Expense Block Entry ----------------------
        with st.container(border=True):
            st.subheader("Add Expense Block")
            st.caption(
                "Each block has **one place, one date, one amount, multiple participants (min 2, max 10), and exactly one payer**."
            )

            disabled = st.session_state.people.shape[0] < 2
            if disabled:
                st.warning("Add **at least 2 people** to create an expense block.")

            with st.form("expense_block_form", clear_on_submit=True, border=False):
                # Place / Date / Amount
                c1, c2 = st.columns([2, 1])
                place = c1.text_input("Place (required)", placeholder="e.g., Cafe Mavi")
                when = c2.date_input("Date", value=date.today(), format="YYYY-MM-DD")

                c3, c4 = st.columns([1, 1])
                amount = c3.number_input("Amount", min_value=0.0, step=1.0, format="%.2f")

                names = st.session_state.people.sort_values("name")["name"].tolist()
                c5, c6 = st.columns([2, 1])
                participants = c5.multiselect(
                    "Participants (2–10)",
                    options=names,
                    placeholder="Select people...",
                    max_selections=10,
                    disabled=disabled,
                )
                payer = c6.selectbox(
                    "Payer (1 person)",
                    options=["— choose —"] + names,
                    index=0,
                    disabled=disabled,
                )

                submit = st.form_submit_button("Add expense block", disabled=disabled)

                if submit:
                    errors = []
                    if not place.strip():
                        errors.append("Place is required.")
                    if amount <= 0:
                        errors.append("Amount must be greater than 0.")
                    if len(participants) < 2:
                        errors.append("Select at least 2 participants.")
                    if payer == "— choose —":
                        errors.append("Select a payer.")
                    if errors:
                        for e in errors:
                            st.error(e)
                    else:
                        # Store a single row; participants kept as a list of names (no ids)
                        new_row = pd.DataFrame(
                            [{
                                "date": when.isoformat(),      # date-only
                                "place": place.strip(),
                                "amount": float(amount),
                                "payer": payer,
                                "participants": participants[:],  # copy the list
                            }]
                        )
                        st.session_state.expenses = pd.concat(
                            [st.session_state.expenses, new_row], ignore_index=True
                        )
                        st.success(
                            f"Added • **{place}** on **{when.isoformat()}** • "
                            f"Amount **{fmt_money(amount)}** • Payer **{payer}** • "
                            f"Participants **{', '.join(participants)}**"
                        )
                        st.toast("Expense saved", icon="✅")

        # ---------------------- UI: Current Blocks (Preview) ----------------------
        if st.session_state.expenses.empty:
            st.info("No expense blocks yet.")
        else:
            st.subheader("Blocks (Preview)")
            view = st.session_state.expenses.copy()

            # For display
            view["Participants (#)"] = view["participants"].apply(lambda lst: len(lst) if isinstance(lst, list) else 0)
            view["Participants"] = view["participants"].apply(lambda lst: ", ".join(lst) if isinstance(lst, list) else "")
            view["Amount"] = view["amount"].map(fmt_money)

            show = view[["date", "place", "Amount", "payer", "Participants (#)", "Participants"]]
            show = show.rename(
                columns={
                    "date": "Date",
                    "place": "Place",
                    "payer": "Payer",
                }
            )

            st.dataframe(show, use_container_width=True, hide_index=True)

            # Downloads (optional)
            c1, c2 = st.columns(2)
            c1.download_button(
                "⬇️ Download expenses.csv",
                data=st.session_state.expenses.to_csv(index=False).encode("utf-8"),
                mime="text/csv",
                file_name="expenses.csv",
            )
            c2.download_button(
                "⬇️ Download people.csv",
                data=st.session_state.people.to_csv(index=False).encode("utf-8"),
                mime="text/csv",
                file_name="people.csv",
            )

        st.caption(
            "Notes: No identifiers are stored; only names. All dates are date-only. "
            "Participants are saved per block as a list of names. Uses only pandas + session_state."
        )

        
        st.divider()


        st.header("🧮 Reconciliation")

        if st.session_state.expenses.empty:
            st.info("No expenses to reconcile yet.")
        else:
            nets = compute_nets(st.session_state.expenses)

            if nets.empty or nets.abs().sum() == 0:
                st.success("Everyone is settled. No transfers needed.")
            else:
                # Show per-person summary
                nets_df = pd.DataFrame({
                    "Person": nets.index,
                    "Net": [to_money_str(v) for v in nets.values],
                    "Status": ["is owed" if v > 0 else ("owes" if v < 0 else "even") for v in nets.values],
                }).sort_values("Net", key=lambda s: s.str.replace(",","").astype(float), ascending=True)

                st.subheader("Per-person nets")
                st.dataframe(nets_df, hide_index=True, use_container_width=True)

                # Settlement plan
                transfers = greedy_settlement(nets)
                if not transfers:
                    st.success("No transfers necessary.")
                else:
                    plan = pd.DataFrame(
                        [{"From": f, "To": t, "Amount": to_money_str(a)} for (f, t, a) in transfers]
                    )
                    st.subheader("Settlement plan")
                    st.dataframe(plan, hide_index=True, use_container_width=True)

                    # Quick checks
                    total_positive = sum(v for v in nets.values if v > 0)
                    total_transfers = sum(a for _, _, a in transfers)
                    st.caption(
                        f"Checks: sum(creditors) = {to_money_str(total_positive)} • "
                        f"sum(transfers) = {to_money_str(total_transfers)}"
                    )



def show(navigate_to):
    st.title("Latest Entries")

    display_menu_buttons(navigate_to)

    calculation_tabs()








def d(x) -> Decimal:
    return Decimal(str(x))

def q2(x: Decimal) -> Decimal:
    # round half up to cents
    return x.quantize(CENT, rounding=ROUND_HALF_UP)

# settlement_logic.py
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Tuple
import pandas as pd

CENT = Decimal("0.01")
def D(x): return Decimal(str(x))
def q2(x: Decimal) -> Decimal: return x.quantize(CENT, rounding=ROUND_HALF_UP)

def split_shares(amount: Decimal, participants: List[str], payer: str) -> Dict[str, Decimal]:
    """Equal split across participants (payer auto-included); rounding remainder to payer's share."""
    if payer not in participants:
        participants = participants + [payer]
    n = len(participants)
    base = q2(amount / n)
    shares = {p: base for p in participants}
    # fix rounding drift by giving the tiny remainder to payer
    drift = amount - sum(shares.values(), start=Decimal("0"))
    shares[payer] = q2(shares[payer] + drift)
    return shares  # each person's share for THIS expense

def per_expense_iou(expense_row: dict) -> List[Tuple[str, str, Decimal]]:
    """
    For a single expense (date/place/amount/payer/participants),
    return IOUs as (debtor -> creditor=payer, amount).
    Payer never appears as debtor here.
    """
    amt = q2(D(expense_row["amount"]))
    payer = expense_row["payer"]
    parts = list(dict.fromkeys(expense_row["participants"]))
    shares = split_shares(amt, parts, payer)
    ious = []
    for p, share in shares.items():
        if p == payer:
            continue  # payer does not owe anyone for this entry
        if share > 0:
            ious.append((p, payer, share))
    return ious

def compute_nets(expenses_df: pd.DataFrame) -> pd.Series:
    """
    Build nets from per-expense IOUs. Positive net => person is owed overall.
    Negative net => person owes overall.
    """
    if expenses_df.empty:
        return pd.Series(dtype="object")

    nets: Dict[str, Decimal] = {}
    for _, row in expenses_df.iterrows():
        for debtor, creditor, amount in per_expense_iou(row.to_dict()):
            nets[debtor]   = q2(nets.get(debtor,   Decimal("0")) - amount)
            nets[creditor] = q2(nets.get(creditor, Decimal("0")) + amount)

    # clean tiny -0.00
    nets = {k: (Decimal("0.00") if abs(v) < Decimal("0.005") else q2(v)) for k, v in nets.items()}
    return pd.Series(nets, dtype="object")

def greedy_settlement(nets: pd.Series) -> List[Tuple[str, str, Decimal]]:
    """Minimal, easy-to-audit transfer list from nets."""
    creditors = [(p, v) for p, v in nets.items() if v > 0]
    debtors   = [(p, -v) for p, v in nets.items() if v < 0]
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    transfers = []
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        d_name, d_amt = debtors[i]
        c_name, c_amt = creditors[j]
        pay = q2(min(d_amt, c_amt))
        if pay > 0:
            transfers.append((d_name, c_name, pay))
            d_amt = q2(d_amt - pay)
            c_amt = q2(c_amt - pay)
        if d_amt == 0: i += 1
        else: debtors[i] = (d_name, d_amt)
        if c_amt == 0: j += 1
        else: creditors[j] = (c_name, c_amt)
    return transfers


def to_money_str(x: Decimal) -> str:
    return f"{float(x):,.2f}"
