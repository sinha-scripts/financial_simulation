import json
import streamlit as st


def save_params(params, filename):
    """Save sidebar parameters to a JSON file."""
    with open(filename, "w") as f:
        json.dump(params, f)


def load_params_from_file(uploaded_file):
    """Load sidebar parameters from an uploaded JSON file."""
    if uploaded_file is not None:
        try:
            return json.load(uploaded_file)
        except json.JSONDecodeError:
            st.sidebar.error("Invalid JSON file format.")
    return {}
