from fastapi import APIRouter, HTTPException, Depends
from app.models import FinanceCalcRequest, FinanceCalcResponse
from app.finance import simulate_loan, simulate_savings
import os

router = APIRouter(prefix="/api/v1/finance", tags=["finance"])

DB_PATH = os.getenv("DB_PATH", "./data/app.db")

@router.post("/calculate", response_model=FinanceCalcResponse)
def calculate(req: FinanceCalcRequest):
    t = req.type.lower()
    p = req.params
    try:
        if t == "loan":
            res = simulate_loan(
                principal=float(p["principal"]),
                annual_rate_pct=float(p["annual_rate_pct"]),
                term_months=int(p["term_months"])
            )
            explanation = f"Simulação de empréstimo: parcela mensal de R$ {res['monthly_payment']}"
        elif t == "savings":
            res = simulate_savings(
                principal=float(p.get("principal", 0)),
                annual_rate_pct=float(p["annual_rate_pct"]),
                term_months=int(p["term_months"]),
                monthly_contribution=float(p.get("monthly_contribution", 0))
            )
            explanation = f"Valor futuro aproximado: R$ {res['future_value']}"
        else:
            raise HTTPException(status_code=400, detail="Tipo de cálculo desconhecido")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Parâmetro faltando: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"result": res, "explanation": explanation}