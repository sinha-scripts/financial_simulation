import streamlit as st
import matplotlib.pyplot as plt
from utils import save_params, load_params_from_file
from simulation import financial_simulation
from sidebar_parameters import get_sidebar_inputs


def initialize_session_state():
    """Ensure session state variables are initialized."""
    if "params" not in st.session_state:
        st.session_state.params = {}
    if "config_loaded" not in st.session_state:
        st.session_state.config_loaded = False
    if "fig" not in st.session_state:
        st.session_state.fig, st.session_state.ax = plt.subplots(figsize=(10, 5))


def load_parameters():
    """Handles file upload and loading of parameters from JSON."""
    uploaded_file = st.sidebar.file_uploader("Upload JSON file to load parameters", type=["json"])
    if uploaded_file and not st.session_state.config_loaded:
        st.session_state.config_loaded = True
        uploaded_params = load_params_from_file(uploaded_file)
        if uploaded_params:
            st.session_state.params = uploaded_params
            st.sidebar.success("Loaded parameters from file!")
        else:
            st.sidebar.warning("File loaded but contains no valid parameters!")
        st.rerun()


def save_parameters(inputs):
    """Saves parameters to a user-specified JSON file."""
    filename = st.sidebar.text_input("Enter filename to save", value="defaults.json")
    if st.sidebar.button("Save Parameters"):
        # Ensure filename ends with .json
        if not filename.lower().endswith(".json"):
            filename += ".json"
        # Convert percentage values back to whole numbers before saving
        formatted_inputs = inputs.copy()
        formatted_inputs["salary_growth_rate"] *= 100
        formatted_inputs["pre_retirement_investment_growth_rate"] *= 100
        formatted_inputs["post_retirement_investment_growth_rate"] *= 100
        formatted_inputs["inflation_rate"] *= 100
        # Save the parameters
        save_params(formatted_inputs, filename)
        st.sidebar.success(f"Parameters saved as {filename}!")


def run_simulation(inputs, extra_expenses_dict):
    """Runs the financial simulation and plots the results."""
    years, corpus = financial_simulation(
        inputs["starting_corpus"],
        inputs["salary"],
        inputs["salary_growth_rate"],
        inputs["pre_retirement_investment_growth_rate"],
        inputs["post_retirement_investment_growth_rate"],
        inputs["inflation_rate"],
        inputs["pre_retirement_expenses"],
        inputs["post_retirement_expenses"],
        inputs["retirement_age"],
        inputs["current_age"],
        inputs["life_expectancy"],
        extra_expenses_dict,
        inputs["adjust_for_inflation"],
    )
    fig, ax = st.session_state.fig, st.session_state.ax
    y_label = "Corpus (Cr) [Real Value]" if inputs["adjust_for_inflation"] else "Corpus (Cr) [Nominal Value]"
    ax.clear()
    ax.plot(years, corpus / 1e7, label=y_label, color="b")  # type:ignore
    ax.axvline(inputs["retirement_age"], color="r", linestyle="--", label="Retirement Age")  # type:ignore
    ax.axhline(0, color="black", linewidth=0.5)  # type:ignore
    ax.set_xlabel("Age")  # type:ignore
    ax.set_ylabel(y_label)  # type:ignore
    ax.set_title("Financial Planning Simulation")  # type:ignore
    ax.legend()  # type:ignore
    ax.grid()  # type:ignore
    st.pyplot(fig)  # type:ignore


def main():
    """Main function to run the Streamlit app."""
    st.title("Financial Planning Simulator")
    initialize_session_state()
    inputs, extra_expenses_dict = get_sidebar_inputs()
    save_parameters(inputs)
    load_parameters()
    run_simulation(inputs, extra_expenses_dict)


if __name__ == "__main__":
    main()
