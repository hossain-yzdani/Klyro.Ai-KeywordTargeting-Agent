from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from ..state import KeywordTargetingState, ContentBrief
from ..schemas.brief_schema import SingleBriefOutput

def brief_node(state: KeywordTargetingState, llm) -> Dict[str, Any]:
  """
  تولید بریف محتوایی سئومحور برای خوشه‌هایی که بالاترین امتیاز اولویت را دارند.
  """
  clusters = state.get("clusters", [])
  briefs: List[ContentBrief] = []

  top_clusters = clusters[:3]

  prompt = ChatPromptTemplate.from_messages([
    (
      "system",
      "شما استراتژیست ارشد سئو و معمار محتوا هستید. "
      "بر اساس اطلاعات کلاستر و کلمات کلیدی، یک سند بریف اجرایی دقیق برای نویسنده محتوا آماده کنید.\n"
      "نکات الزامی:\n"
      "- عنوان سئو و متا دیسکریپشن باید جذاب و نرخ کلیک‌محور (CTR-oriented) باشند.\n"
      "- ساختار هدینگ‌ها (H2 و H3) باید جریان منطقی پوشش موضوع را رعایت کند.\n"
      "- سوالات متداول باید پاسخ‌دهنده دغدغه‌های واقعی جستجوگران باشند.\n"
      "- خروجی باید کاملاً مطابق با ساختار JSON باشد."
    ),
    (
      "user",
      "حوزه بازار: {market}\n"
      "نام خوشه: {name}\n"
      "نوع صفحه هدف: {page_type}\n"
      "نیت غالب جستجو: {intent}\n"
      "کلمات کلیدی خوشه: {keywords}"
    )
  ])

  structured_llm = llm.with_structured_output(SingleBriefOutput, method="json_mode")
  chain = prompt | structured_llm

  for cluster in top_clusters:
    try:
      res: SingleBriefOutput = chain.invoke({
        "market": state.get("market", "عمومی"),
        "name": cluster.name,
        "page_type": cluster.recommended_page_type,
        "intent": cluster.dominant_intent,
        "keywords": "، ".join(cluster.keywords[:10])
      })

      briefs.append(
        ContentBrief(
          cluster_name=res.cluster_name,
          page_type=res.page_type,
          seo_title=res.seo_title,
          h1=res.h1,
          meta_description=res.meta_description,
          headings_structure=res.headings_structure,
          faqs=res.faqs,
          internal_linking_suggestions=res.internal_linking_suggestions
        )
      )
    except Exception as e:
      continue

  log_msg = f"[brief] تعداد {len(briefs)} بریف کامل برای اولویت‌های برتر تولید شد."

  return {
    "briefs": briefs,
    "logs": state.get("logs", []) + [log_msg]
  }