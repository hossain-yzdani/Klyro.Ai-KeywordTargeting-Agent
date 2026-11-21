from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class KeywordIntentOutput(BaseModel):
  model_config = ConfigDict(extra="forbid")

  intent: Literal[
    "Informational",
    "Commercial",
    "Transactional",
    "Navigational"
  ] = Field(
    description="نیت اصلی کاربر از جستجوی این کلمه کلیدی"
  )

  confidence: float = Field(
    default=1.0,
    ge=0.0,
    le=1.0,
    description="میزان اطمینان مدل از این دسته‌بندی"
  )


class ClusterNamingOutput(BaseModel):
  model_config = ConfigDict(extra="forbid")

  cluster_name: str = Field(
    description="نام موضوعی، دقیق و سئومحور برای این دسته از کلمات کلیدی (حداکثر ۴ کلمه)"
  )


class MarketDiscoveryOutput(BaseModel):
  model_config = ConfigDict(extra="forbid")

  identified_market: str = Field(
    description="عنوان دقیق بازار و حوزه فعالیت شناسایی‌شده"
  )

  core_competitors: list[str] = Field(
    description="فهرست نام رقبای اصلی بازار؛ هر عضو فقط یک رشته متنی باشد"
  )

  seed_keywords: list[str] = Field(
    description="حداقل ۵ کلمه کلیدی پایه و مرتبط با بازار"
  )


class KeywordExpansionItem(BaseModel):
  model_config = ConfigDict(extra="forbid")

  seed_keyword: str = Field(
    description="کلمه کلیدی پایه‌ای که این عبارات از آن استخراج شده‌اند"
  )

  related_searches: list[str] = Field(
    description="عبارات مرتبطی که کاربران جستجو می‌کنند"
  )

  common_questions: list[str] = Field(
    description="سؤالات رایج کاربران درباره این موضوع"
  )

  long_tail_phrases: list[str] = Field(
    description="عبارات کلیدی طولانی و مشخص مرتبط با کلمه پایه"
  )


class ExpandKeywordsOutput(BaseModel):
  model_config = ConfigDict(extra="forbid")

  expansions: list[KeywordExpansionItem] = Field(
    description="فهرست گسترش کلمات کلیدی، به تفکیک هر کلمه پایه"
  )
