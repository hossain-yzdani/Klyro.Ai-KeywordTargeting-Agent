from typing import Dict, Any, List
from collections import Counter
from sklearn.cluster import AgglomerativeClustering
from langchain_core.prompts import ChatPromptTemplate
from ..state import KeywordTargetingState, ClusterSummary
from ..schemas.cluster_schema import ClusterNamingOutput

def cluster_node(state: KeywordTargetingState, embedding_model, llm) -> Dict[str, Any]:
  """
  خوشه‌بندی معنایی کلمات کلیدی:
  ۱. تولید بردارهای معنایی با Embedding
  ۲. خوشه‌بندی سلسله‌مراتبی با الگوریتم Agglomerative Clustering
  ۳. نام‌گذاری هوشمند دسته‌ها توسط LLM
  """
  processed = state.get("processed_keywords", [])
  
  if not processed:
    return {"clusters": []}

  texts = [item.normalized for item in processed]

  embeddings = embedding_model.embed_documents(texts)

  clustering = AgglomerativeClustering(
    n_clusters=None,
    distance_threshold=0.4,
    metric='cosine',
    linkage='average'
  )
  labels = clustering.fit_predict(embeddings)

  clusters_dict: Dict[int, List[int]] = {}
  for idx, label in enumerate(labels):
    clusters_dict.setdefault(int(label), []).append(idx)
    processed[idx].cluster_id = int(label)

  name_prompt = ChatPromptTemplate.from_messages([
    (
      "system",
      "شما مدیر استراتژی محتوا هستید. با بررسی کلمات کلیدی یک خوشه، "
      "یک عنوان موضوعی دقیق، شفاف و سئومحور (کمتر از ۴ کلمه) به زبان فارسی برای این گروه انتخاب کنید."
    ),
    (
      "user",
      "کلمات کلیدی این خوشه عبارتند از:\n{keywords}"
    )
  ])
  
  structured_naming = llm.with_structured_output(ClusterNamingOutput)
  naming_chain = name_prompt | structured_naming

  cluster_summaries: List[ClusterSummary] = []

  for c_id, item_indices in clusters_dict.items():
    c_keywords = [texts[i] for i in item_indices]
    sample_keywords = c_keywords[:8]

    try:
      res: ClusterNamingOutput = naming_chain.invoke({
        "keywords": "، ".join(sample_keywords)
      })
      c_name = res.cluster_name
    except Exception:
      c_name = sample_keywords[0]

    for i in item_indices:
      processed[i].cluster_name = c_name

    intents = [processed[i].intent for i in item_indices if processed[i].intent]
    dominant_intent = Counter(intents).most_common(1)[0][0] if intents else "Informational"

    page_type = "Pillar" if len(c_keywords) >= 5 else "Cluster"

    cluster_summaries.append(
      ClusterSummary(
        id=c_id,
        name=c_name,
        keywords=c_keywords,
        dominant_intent=dominant_intent,
        recommended_page_type=page_type
      )
    )

  log_msg = f"[cluster] تعداد {len(processed)} عبارت در قالب {len(cluster_summaries)} خوشه موضوعی متمایز دسته‌بندی و نام‌گذاری شدند."

  return {
    "processed_keywords": processed,
    "clusters": cluster_summaries,
    "logs": state.get("logs", []) + [log_msg]
  }