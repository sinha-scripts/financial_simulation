import streamlit as st


def get_sidebar_inputs():
    """Handles sidebar input collection and updates session state parameters."""
    params = st.session_state.params
    inputs = {
        "starting_corpus": st.sidebar.number_input(
            "Starting Corpus (₹)",
            value=params.get("starting_corpus", 1e7),
            step=1e6,
            format="%.0f",
        ),
        "salary": st.sidebar.number_input(
            "Annual Salary (₹)",
            value=params.get("salary", 3e6),
            step=1e5,
            format="%.0f",
        ),
        "salary_growth_rate": st.sidebar.slider(
            "Salary Growth Rate (%)",
            0.0,
            15.0,
            params.get("salary_growth_rate", 6.0),
            0.1,
        )
        / 100,
        "pre_retirement_investment_growth_rate": st.sidebar.slider(
            "Pre-Retirement Investment Growth Rate (%)",
            5.0,
            15.0,
            params.get("pre_retirement_investment_growth_rate", 10.0),
            0.1,
        )
        / 100,
        "post_retirement_investment_growth_rate": st.sidebar.slider(
            "Post-Retirement Investment Growth Rate (%)",
            3.0,
            12.0,
            params.get("post_retirement_investment_growth_rate", 7.0),
            0.1,
        )
        / 100,
        "inflation_rate": st.sidebar.slider("Inflation Rate (%)", 2.0, 10.0, params.get("inflation_rate", 5.0), 0.1)
        / 100,
        "pre_retirement_expenses": st.sidebar.number_input(
            "Annual Pre-Retirement Expenses (₹)",
            value=params.get("pre_retirement_expenses", 1e6),
            step=1e5,
            format="%.0f",
        ),
        "post_retirement_expenses": st.sidebar.number_input(
            "Annual Post-Retirement Expenses (₹)",
            value=params.get("post_retirement_expenses", 1e6),
            step=1e5,
            format="%.0f",
        ),
        "retirement_age": st.sidebar.slider("Retirement Age", 40, 70, params.get("retirement_age", 55), 1),
        "current_age": st.sidebar.slider("Current Age", 20, 50, params.get("current_age", 27), 1),
        "life_expectancy": st.sidebar.slider("Life Expectancy", 70, 100, params.get("life_expectancy", 85), 1),
        "adjust_for_inflation": st.sidebar.checkbox(
            "Adjust for Inflation", value=params.get("adjust_for_inflation", True)
        ),
    }
    # Handling extra expenses
    extra_expenses_str = st.sidebar.text_area(
        "Extra Expenses (Format: age1:amount1, age2:amount2)",
        params.get("extra_expenses_str", ""),
    )
    inputs["extra_expenses_str"] = extra_expenses_str
    extra_expenses_dict = {}
    if not extra_expenses_str:
        return inputs, {}
    try:
        for item in extra_expenses_str.split(","):
            age, amount = map(float, item.split(":"))
            extra_expenses_dict[int(age)] = amount
    except ValueError:
        st.sidebar.warning("Invalid format for extra expenses. Use: age1:amount1, age2:amount2")
    return inputs, extra_expenses_dict
