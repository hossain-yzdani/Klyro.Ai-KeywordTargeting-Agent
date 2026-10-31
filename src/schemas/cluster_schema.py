from typing import Literal
from pydantic import BaseModel, Field

class KeywordIntentOutput(BaseModel):
  intent: Literal["Informational", "Commercial", "Transactional", "Navigational"] = Field(
    description="نیت اصلی کاربر از جستجوی این کلمه کلیدی"
  )
  confidence: float = Field(
    default=1.0, 
    ge=0.0, 
    le=1.0, 
    description="میزان اطمینان مدل از این دسته‌بندی از ۰ تا ۱"
  )