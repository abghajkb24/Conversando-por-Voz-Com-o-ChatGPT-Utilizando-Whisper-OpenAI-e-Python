from pydantic import BaseModel, Field
from typing import Optional, Dict

class FinanceCalcRequest(BaseModel):
    type: str = Field(..., description="loan|savings|installment")
    params: Dict

class FinanceCalcResponse(BaseModel):
    result: Dict
    explanation: Optional[str]