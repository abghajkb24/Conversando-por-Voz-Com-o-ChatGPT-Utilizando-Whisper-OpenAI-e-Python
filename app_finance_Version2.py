"""
Módulo financeiro: cálculos e validações.
Funções principais:
- simulate_loan(principal, annual_rate_pct, term_months) -> dict
- simulate_savings(principal, annual_rate_pct, term_months, contribution=0) -> dict
- helpers: juros compostos, PMT
"""
from typing import Dict
import math

def pmt(rate_per_period: float, n_periods: int, pv: float) -> float:
    """Payment per period (PMT). rate_per_period as decimal (e.g., 0.01)."""
    if rate_per_period == 0:
        return pv / n_periods
    return (pv * rate_per_period) / (1 - (1 + rate_per_period) ** -n_periods)

def simulate_loan(principal: float, annual_rate_pct: float, term_months: int, compounding: str = "monthly") -> Dict:
    if principal <= 0 or term_months <= 0:
        raise ValueError("principal and term_months must be positive")
    if annual_rate_pct < 0:
        raise ValueError("annual_rate_pct must be non-negative")
    # Convert annual rate to monthly decimal
    monthly_rate = annual_rate_pct / 100.0 / 12.0
    payment = pmt(monthly_rate, term_months, principal)
    total_payment = payment * term_months
    total_interest = total_payment - principal
    return {
        "monthly_payment": round(payment, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "annual_rate_pct": annual_rate_pct,
        "term_months": term_months,
        "principal": principal
    }

def simulate_savings(principal: float, annual_rate_pct: float, term_months: int, monthly_contribution: float = 0.0) -> Dict:
    if term_months <= 0:
        raise ValueError("term_months must be positive")
    monthly_rate = annual_rate_pct / 100.0 / 12.0
    fv = principal * (1 + monthly_rate) ** term_months
    if monthly_contribution:
        fv += monthly_contribution * (((1 + monthly_rate) ** term_months - 1) / monthly_rate)
    return {
        "future_value": round(fv, 2),
        "principal": principal,
        "monthly_contribution": monthly_contribution,
        "annual_rate_pct": annual_rate_pct,
        "term_months": term_months
    }