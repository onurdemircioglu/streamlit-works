from datetime import date
import streamlit as st
import pandas as pd


def smart_selectbox_v1(label, options, key, default=None):
    if not options:
        st.warning(f"No options available for '{label}'")
        return ""  # ✅ Return empty string instead of None

    if default is None:
        default = options[0]

    default_index = 0
    if key in st.session_state:
        try:
            default_index = options.index(st.session_state[key])
        except ValueError:
            default_index = options.index(default) if default in options else 0

    return st.selectbox(label, options=options, index=default_index, key=key)


def smart_selectbox(label, options, key, default=None):
    # ✅ Convert Series to list
    if isinstance(options, (pd.Series, pd.Index)):
        options = options.tolist()

    if not options:  # Now safe to check emptiness
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


def smart_number_input_v1(label, key, default=0.0, min_value=0.0, max_value=None, step=1.0, format="%.2f"):
    value = st.session_state.get(key, default)
    return st.number_input(label, min_value=min_value, max_value=max_value, step=step, format=format, value=value, key=key)

def smart_number_input_v2(label, key, default=0.0, min_value=None, max_value=None, step=None, format=None):
    value = st.session_state.get(key, default)
    return st.number_input(label, value=value, key=key,
                           min_value=min_value, max_value=max_value,
                           step=step, format=format)

def smart_number_input(label, key, default=None, min_value=None, max_value=None, step=None, format=None):
    # ✅ Automatically choose the highest between default and min_value
    if default is None:
        default = min_value if min_value is not None else 0.0
    elif min_value is not None and default < min_value:
        default = min_value

    value = st.session_state.get(key, default)
    return st.number_input(label, value=value, key=key, min_value=min_value, max_value=max_value, step=step, format=format)



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



    #def clear_field(field_key: str, default_value=""):
    #def clear_field(field_key: str, default_value=""):
        """
        Clears the value of a Streamlit widget by resetting its session state.
        :param field_key: The key assigned to the widget.
        :param default_value: The value to reset to (default is an empty string).
        """
        #if field_key in st.session_state:
            #st.session_state[field_key] = default_value""