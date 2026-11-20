from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from ..state import KeywordTargetingState
from ..schemas.cluster_schema import ExpandKeywordsOutput

def expand_node(state: KeywordTargetingState, llm) -> Dict[str, Any]:
  """
  گسترش کلمات اولیه به لانگ‌تیل‌ها و سوالات متداول کاربران
  """
  raw_keywords = state.get("raw_keywords", [])

  prompt = ChatPromptTemplate.from_messages([
    (
      "system",
      "برای این لیست از کلمات کلیدی، کلمات مرتبط جستجوشده توسط کاربران فارسی‌زبان، "
      "پرسش‌های رایج (چگونه، چیست، راهنمای و...) و عبارات لانگ‌تیل را استخراج کنید."
    ),
    (
      "user",
      "کلمات پایه: {seeds}\n"
      "بازار هدف: {market}"
    )
  ])

  structured_llm = llm.with_structured_output(ExpandKeywordsOutput)
  chain = prompt | structured_llm

  sample_seeds = raw_keywords[:10]

  res: ExpandKeywordsOutput = chain.invoke({
    "seeds": "، ".join(sample_seeds),
    "market": state.get("market", "")
  })

  updated_raw = list(set(raw_keywords + res.expanded_keywords))

  log_msg = f"[expand] تعداد کلمات خام پس از بسط به {len(updated_raw)} عبارت رسید."

  return {
    "raw_keywords": updated_raw,
    "logs": state.get("logs", []) + [log_msg]
  }