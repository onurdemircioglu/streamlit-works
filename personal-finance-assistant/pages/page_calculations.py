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




def show(navigate_to):
    st.title("Latest Entries")

    display_menu_buttons(navigate_to)




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
