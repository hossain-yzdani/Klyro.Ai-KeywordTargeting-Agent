from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from ..state import KeywordTargetingState
from ..schemas.cluster_schema import ExpandKeywordsOutput


def expand_node(state: KeywordTargetingState, llm) -> Dict[str, Any]:
  """
  گسترش کلمات اولیه به عبارات مرتبط، سؤالات متداول و لانگ‌تیل‌ها
  """

  raw_keywords = state.get("raw_keywords", [])
  sample_seeds = raw_keywords[:10]

  if not sample_seeds:
    return {
      "logs": state.get("logs", []) + [
        "[expand] هیچ کلمه کلیدی برای گسترش وجود نداشت."
      ]
    }

  prompt = ChatPromptTemplate.from_messages([
    (
    "system",
    """
    شما یک متخصص تحقیق کلمات کلیدی و استراتژیست سئو هستید.

    خروجی شما باید حتماً در قالب JSON معتبر باشد.
    تمام پاسخ را فقط به صورت JSON و بدون Markdown یا توضیحات اضافی برگردانید.

    برای هر کلمه کلیدی پایه، موارد زیر را استخراج کنید:

    1. related_searches:
      عبارت‌های مرتبطی که کاربران جستجو می‌کنند.

    2. common_questions:
      سؤالات واقعی و رایج کاربران درباره موضوع.

    3. long_tail_phrases:
      عبارات طولانی و هدفمند مرتبط با موضوع.

    قوانین:
    - تمام خروجی‌ها باید فارسی باشند.
    - از تولید عبارات تکراری خودداری کنید.
    - عبارات باید با بازار هدف مرتبط باشند.
    - کلمات کلیدی پایه را با یکدیگر ترکیب نکنید.
    - از ساختن آمار، حجم جستجو یا اطلاعات تأییدنشده خودداری کنید.
    - سال‌های قدیمی یا تاریخ‌های ساختگی وارد عبارات نکنید.

    ساختار JSON مورد انتظار:

    {{
      "expansions": [
        {{
          "seed_keyword": "کلمه پایه",
          "related_searches": [],
          "common_questions": [],
          "long_tail_phrases": []
        }}
      ]
    }}
    """
    ),
    (
      "user",
      """
      کلمات پایه:
      {seeds}

      بازار هدف:
      {market}
      """
    )
  ])

  structured_llm = llm.with_structured_output(
    ExpandKeywordsOutput,
    method="json_mode"
  )

  chain = prompt | structured_llm

  res: ExpandKeywordsOutput = chain.invoke({
    "seeds": "\n".join(sample_seeds),
    "market": state.get("market", "")
  })

  expanded_keywords = []

  for item in res.expansions:
    expanded_keywords.extend(item.related_searches)
    expanded_keywords.extend(item.common_questions)
    expanded_keywords.extend(item.long_tail_phrases)

  updated_raw = list(dict.fromkeys(
    raw_keywords + expanded_keywords
  ))

  log_msg = (
    f"[expand] تعداد {len(expanded_keywords)} عبارت جدید تولید شد؛ "
    f"تعداد کل کلمات خام: {len(updated_raw)}"
  )

  return {
    "raw_keywords": updated_raw,
    "logs": state.get("logs", []) + [log_msg]
  }