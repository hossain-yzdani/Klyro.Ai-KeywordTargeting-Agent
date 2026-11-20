from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from ..state import KeywordTargetingState
from ..schemas.cluster_schema import MarketDiscoveryOutput

def discover_node(state: KeywordTargetingState, llm) -> Dict[str, Any]:
  """
  استخراج کلمات کلیدی بذر (Seed) و رقبای احتمالی بر اساس کانتکست سایت
  """
  prompt = ChatPromptTemplate.from_messages([
    (
      "system",
      "شما تحلیل‌گر بازار دیجیتال و استراتژیست سئو هستید. "
      "بر اساس اطلاعات سایت و بازار هدف، حوزه دقیق مخاطب، رقبای احتمالی "
      "و کلمات کلیدی بذر (Seed Keywords) را مشخص کنید."
    ),
    (
      "user",
      "آدرس دامنه: {domain}\n"
      "بازار و حوزه فعالیت: {market}\n"
      "موضوع یا تم هدف: {target_theme}"
    )
  ])

  structured_llm = llm.with_structured_output(MarketDiscoveryOutput)
  chain = prompt | structured_llm

  res: MarketDiscoveryOutput = chain.invoke({
    "domain": state.get("domain", ""),
    "market": state.get("market", ""),
    "target_theme": state.get("target_theme", "")
  })

  current_raw = state.get("raw_keywords", [])
  combined_raw = list(set(current_raw + res.seed_keywords))

  log_msg = f"[discover] تعداد {len(res.seed_keywords)} کلمه بذر اولیه برای بازار '{res.identified_market}' ایجاد شد."

  return {
    "raw_keywords": combined_raw,
    "logs": state.get("logs", []) + [log_msg]
  }