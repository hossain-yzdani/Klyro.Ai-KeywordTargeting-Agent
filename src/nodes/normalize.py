from typing import List, Dict, Any
from ..state import KeywordTargetingState, KeywordItem
from ..utils.text_cleaner import clean_persian_text

def normalize_node(state: KeywordTargetingState) -> Dict[str, Any]:
  """
  ورودی: raw_keywords از وضعیت فعلی
  خروجی: لیست ساختاریافته processed_keywords بدون تکرار و تمیزشده
  """
  raw_keywords = state.get("raw_keywords", [])
  seen = set()
  processed_items: List[KeywordItem] = []

  for kw in raw_keywords:
    normalized = clean_persian_text(kw)
    
    if normalized and normalized not in seen:
      seen.add(normalized)
      processed_items.append(
        KeywordItem(
          raw=kw,
          normalized=normalized
        )
      )

  log_message = f"[normalize] تعداد {len(processed_items)} کیورد از مجموع {len(raw_keywords)} مورد تمیز و یکتا شد."

  return {
      "processed_keywords": processed_items,
      "logs": state.get("logs", []) + [log_message]
  }