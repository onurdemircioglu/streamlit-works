from datetime import date
import streamlit as st


def smart_selectbox(label, options, key, default=None):
    if not options:
        st.warning(f"No options available for '{label}'")
        return None

    if default is None:
        default = options[0]

    default_index = 0
    if key in st.session_state:
        try:
            default_index = options.index(st.session_state[key])
        except ValueError:
            default_index = options.index(default) if default in options else 0

    return st.selectbox(label, options=options, index=default_index, key=key)


def smart_text_input(label, key, default=""):
    value = st.session_state.get(key, default)
    return st.text_input(label, value=value, key=key)


def smart_text_area(label, key, default="", height=100):
    value = st.session_state.get(key, default)
    return st.text_area(label, value=value, key=key, height=height)


def smart_number_input(label, key, default=0.0, min_value=0.0, max_value=None, step=1.0, format="%.2f"):
    value = st.session_state.get(key, default)
    return st.number_input(label, min_value=min_value, max_value=max_value, step=step, format=format, value=value, key=key)


def smart_date_input(label, key, default=None):
    if default is None:
        default = date.today()
    value = st.session_state.get(key, default)
    return st.date_input(label, value=value, key=key)


def smart_multiselect(label, options, key, default=None):
    if default is None:
        default = []
    value = st.session_state.get(key, default)
    return st.multiselect(label, options=options, default=value, key=key)


def smart_checkbox(label, key, default=False):
    value = st.session_state.get(key, default)
    return st.checkbox(label, value=value, key=key)


def render_clear_button_with_confirmation(field_keys: list, label: str = "Clear All Fields", checkbox_label: str = "I want to clear all form fields"):
    """
    Renders a clear/reset button with confirmation checkbox.
    Clears all specified keys from st.session_state on click.

    Args:
        field_keys (list): List of keys to clear from session state.
        label (str): Text on the clear button.
        checkbox_label (str): Text on the confirmation checkbox.
    """
    st.markdown("---")
    st.subheader("🧹 Reset Form")

    confirm_clear = st.checkbox(checkbox_label, key="confirm_clear_fields")

    if st.button(f"✅ {label}", disabled=not confirm_clear):
        for key in field_keys:
            st.session_state.pop(key, None)
            st.success("Form cleared")
        st.rerun()
