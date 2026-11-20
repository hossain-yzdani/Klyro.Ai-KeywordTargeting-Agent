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
  
class ClusterNamingOutput(BaseModel):
  cluster_name: str = Field(
    description="نام موضوعی، دقیق و سئومحور برای این دسته از کلمات کلیدی (حداکثر ۴ کلمه)"
  )
  
class MarketDiscoveryOutput(BaseModel):
  identified_market: str = Field(description="عنوان بازار و پرسونای شناسایی‌شده")
  core_competitors: List[str] = Field(description="نام یا حوزه رقبای اصلی بازار")
  seed_keywords: List[str] = Field(description="حداقل ۵ کلمه کلیدی پایه و اصلی برای شروع")