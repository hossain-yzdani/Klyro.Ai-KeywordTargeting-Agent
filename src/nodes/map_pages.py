from typing import Dict, Any, List
from ..state import KeywordTargetingState

def map_pages_node(state: KeywordTargetingState) -> Dict[str, Any]:
  """
  نگاشت خوشه‌ها به معماری صفحات و شناسایی ریسک همنوع‌خواری (Cannibalization):
  - تطبیق کلمات خوشه و عنوان آن با عناوین و آدرس‌های صفحات موجود
  - تصمیم‌گیری برای ساخت صفحه جدید یا بازنویسی/به‌روزرسانی صفحات فعلی
  """
  clusters = state.get("clusters", [])
  existing_pages = state.get("existing_pages", [])
  
  cannibalized_count = 0

  for cluster in clusters:
    competing_pages: List[str] = []
    cluster_tokens = set(cluster.name.lower().split())

    for page in existing_pages:
      page_title = page.get("title", "").lower()
      page_url = page.get("url", "")
      page_tokens = set(page_title.split())

      intersection = cluster_tokens.intersection(page_tokens)
      if len(intersection) >= 2 or cluster.name.lower() in page_title:
        competing_pages.append(f"{page_title} ({page_url})")

    if competing_pages:
      cluster.cannibalization_risk = True
      cluster.competing_pages = competing_pages
      cluster.target_page = f"به‌روزرسانی صفحه فعلی: {competing_pages[0]}"
      cannibalized_count += 1
    else:
      cluster.cannibalization_risk = False
      cluster.competing_pages = []
      cluster.target_page = f"تولید صفحه جدید ({cluster.recommended_page_type})"

  log_msg = (
    f"[map_pages] بررسی صفحات برای {len(clusters)} خوشه انجام شد. "
    f"{cannibalized_count} خوشه دارای تداخل موضوعی با صفحات فعلی سایت شناسایی شدند."
  )

  return {
    "clusters": clusters,
    "logs": state.get("logs", []) + [log_msg]
  }