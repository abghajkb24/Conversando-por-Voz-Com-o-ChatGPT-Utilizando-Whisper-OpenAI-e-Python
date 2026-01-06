import pytest
from app.finance import simulate_loan, simulate_savings

def test_simulate_loan_basic():
    res = simulate_loan(10000, 12, 12)
    # monthly payment should be positive and total_interest > 0
    assert res["monthly_payment"] > 0
    assert res["total_interest"] >= 0
    assert res["principal"] == 10000

def test_simulate_savings_basic():
    res = simulate_savings(1000, 6, 12, monthly_contribution=50)
    assert res["future_value"] > 1000
    assert res["monthly_contribution"] == 50