from typing import Dict, Any
from ..state import KeywordTargetingState

INTENT_WEIGHTS = {
  "Transactional": 1.5,
  "Commercial": 1.2,
  "Informational": 1.0,
  "Navigational": 0.8
}

def prioritize_node(state: KeywordTargetingState) -> Dict[str, Any]:
  """
  محاسبه امتیاز اولویت برای هر خوشه و مرتب‌سازی نهایی:
  فرمول: (مجموع سرچ * ضریب نیت) / میانگین سختی
  """
  clusters = state.get("clusters", [])
  processed = state.get("processed_keywords", [])

  for cluster in clusters:
    cluster_items = [item for item in processed if item.cluster_id == cluster.id]
    
    if not cluster_items:
      cluster.priority_score = 0.0
      continue

    total_volume = sum(item.search_volume for item in cluster_items)
    avg_difficulty = sum(item.difficulty for item in cluster_items) / len(cluster_items)
    
    intent_factor = INTENT_WEIGHTS.get(cluster.dominant_intent, 1.0)

    safe_difficulty = max(avg_difficulty, 1.0)
    
    score = (total_volume * intent_factor) / safe_difficulty
    cluster.priority_score = round(score, 2)

  clusters.sort(key=lambda c: c.priority_score, reverse=True)

  log_msg = f"[prioritize] اولویت‌بندی {len(clusters)} خوشه بر اساس پتانسیل تجاری و سختی رقابت محاسبه شد."

  return {
    "clusters": clusters,
    "logs": state.get("logs", []) + [log_msg]
  }