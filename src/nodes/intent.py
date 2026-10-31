from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from ..state import KeywordTargetingState
from ..schemas.cluster_schema import KeywordIntentOutput

RULE_PATTERNS = {
  "Transactional": [
    "خرید", "سفارش", "قیمت", "رزرو", "ثبت نام", "فروشگاه", "تعرفه", "هزینه"
  ],
  "Commercial": [
    "بهترین", "برترین", "مقایسه", "نقد و بررسی", "بررسی", "تخفیف", "کد تخفیف", "لیست"
  ],
  "Informational": [
    "چیست", "چگونه", "آموزش", "راهنمای", "علت", "روش", "طرز", "چرا", "نحوه"
  ],
  "Navigational": [
    "ورود", "پنل", "سایت", "ادرس", "شماره تماس", "پشتیبانی", "لاگین"
  ]
}

def detect_by_rules(text: str) -> str | None:
  """بررسی سریع با عبارات کلیدی بدون نیاز به مدل"""
  for intent, patterns in RULE_PATTERNS.items():
    if any(p in text for p in patterns):
      return intent
  return None

def intent_node(state: KeywordTargetingState, llm) -> Dict[str, Any]:
  """
  بررسی هیبریدی نیت جستجو:
  ۱. بررسی با الگوهای صریح
  ۲. در صورت ابهام، ارسال به LLM با Structured Output
  """
  processed = state.get("processed_keywords", [])
  
  prompt = ChatPromptTemplate.from_messages([
    (
      "system",
      "شما متخصص سئو و تحلیل رفتار جستجوی کاربران هستید. "
      "وظیفه شما تعیین نیت جستجوی (Search Intent) کلمه کلیدی بر اساس کانتکست بازار است. "
      "نیت‌ها عبارتند از:\n"
      "- Informational: کسب اطلاعات و یادگیری\n"
      "- Commercial: مقایسه، تحقیق و انتخاب محصول یا سرویس\n"
      "- Transactional: اقدام مستقیم به خرید، دانلود یا ثبت‌نام\n"
      "- Navigational: رفتن به یک صفحه، سایت یا آدرس مشخص"
    ),
    (
      "user",
      "حوزه بازار: {market}\nکلمه کلیدی: {keyword}"
    )
  ])
  
  structured_llm = llm.with_structured_output(KeywordIntentOutput)
  intent_chain = prompt | structured_llm

  rule_count = 0
  llm_count = 0

  for item in processed:
    matched = detect_by_rules(item.normalized)
    
    if matched:
      item.intent = matched
      rule_count += 1
    else:
      try:
        res: KeywordIntentOutput = intent_chain.invoke({
          "market": state.get("market", "عمومی"),
          "keyword": item.normalized
        })
        item.intent = res.intent
      except Exception:
        item.intent = "Informational"
      llm_count += 1

  log_msg = (
    f"[intent] تعیین نیت {len(processed)} کلمه: "
    f"{rule_count} مورد از طریق الگوهای متنی، {llm_count} مورد با هوش مصنوعی."
  )

  return {
    "processed_keywords": processed,
    "logs": state.get("logs", []) + [log_msg]
  }