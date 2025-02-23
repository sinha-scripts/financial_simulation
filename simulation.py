import numpy as np


def financial_simulation(
    starting_corpus: int,
    salary: int,
    salary_growth_rate: float,
    pre_retirement_investment_growth_rate: float,
    post_retirement_investment_growth_rate: float,
    inflation_rate: float,
    pre_retirement_expenses: int,
    post_retirement_expenses: int,
    retirement_age: int,
    current_age: int,
    life_expectancy: int,
    extra_expenses_dict: dict[int, float],
    adjust_for_inflation: bool,
):
    years = np.arange(current_age, life_expectancy + 1)
    corpus = np.zeros_like(years, dtype=float)
    corpus[0] = starting_corpus
    salary_arr = salary * (1 + salary_growth_rate) ** (years - current_age)
    expenses_arr = np.where(
        years <= retirement_age,
        pre_retirement_expenses * (1 + inflation_rate) ** (years - current_age),
        post_retirement_expenses * (1 + inflation_rate) ** (years - current_age),
    )
    if adjust_for_inflation:
        salary_arr /= (1 + inflation_rate) ** (years - current_age)
        expenses_arr /= (1 + inflation_rate) ** (years - current_age)
    else:
        extra_expenses_dict = {
            age: amount * ((1 + inflation_rate) ** (age - current_age)) for age, amount in extra_expenses_dict.items()
        }
    for i in range(1, len(years)):
        age = years[i]
        investment_growth_rate = (
            pre_retirement_investment_growth_rate if age <= retirement_age else post_retirement_investment_growth_rate
        )
        if adjust_for_inflation:
            corpus[i] = corpus[i - 1] * (1 + investment_growth_rate) / (1 + inflation_rate)
        else:
            corpus[i] = corpus[i - 1] * (1 + investment_growth_rate)
        if age <= retirement_age:
            corpus[i] += salary_arr[i] - expenses_arr[i]
        else:
            corpus[i] -= expenses_arr[i]
        if age in extra_expenses_dict:
            corpus[i] -= extra_expenses_dict[age]
        if corpus[i] < 0:
            corpus[i] = 0
    return years, corpus
