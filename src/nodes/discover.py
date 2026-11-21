
from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from ..state import KeywordTargetingState
from ..schemas.cluster_schema import MarketDiscoveryOutput


def discover_node(state: KeywordTargetingState, llm) -> Dict[str, Any]:

  prompt = ChatPromptTemplate.from_messages([
    (
      "system",
      """
      شما تحلیل‌گر بازار دیجیتال و استراتژیست حرفه‌ای SEO هستید.

      وظیفه شما تحلیل بازار هدف و استخراج سه خروجی است:

      1. identified_market:
          تعریف دقیق بازار و حوزه فعالیت سایت.

      2. core_competitors:
          فهرست نام رقبای اصلی و مرتبط بازار.
          هر عضو این لیست باید یک رشته متنی باشد، نه یک آبجکت.

      3. seed_keywords:
          حداقل ۵ کلمه کلیدی پایه و مرتبط با بازار.

      قوانین:
      - تمام فیلدهای موردنیاز را تکمیل کنید.
      - از اطلاعات غیرمرتبط و حدس‌های بی‌پایه خودداری کنید.
      - نام فیلدها را تغییر ندهید.
      - برای هر رقیب فقط نام آن را برگردانید.
      - کلمات کلیدی باید متناسب با بازار و مخاطب هدف باشند.
      """
    ),
    (
      "user",
      """
      آدرس دامنه: {domain}

      بازار و حوزه فعالیت: {market}

      موضوع یا تم هدف: {target_theme}
      """
    )
  ])

  structured_llm = llm.with_structured_output(
    MarketDiscoveryOutput,
    method="json_schema",
    strict=True
  )

  chain = prompt | structured_llm

  res: MarketDiscoveryOutput = chain.invoke({
    "domain": state.get("domain", ""),
    "market": state.get("market", ""),
    "target_theme": state.get("target_theme", "")
  })

  current_raw = state.get("raw_keywords", [])

  combined_raw = list(dict.fromkeys(
    current_raw + res.seed_keywords
  ))

  log_msg = (
    f"[discover] تعداد {len(res.seed_keywords)} "
    f"کلمه بذر اولیه برای بازار "
    f"'{res.identified_market}' ایجاد شد."
  )

  return {
    "raw_keywords": combined_raw,
    "logs": state.get("logs", []) + [log_msg]
  }
