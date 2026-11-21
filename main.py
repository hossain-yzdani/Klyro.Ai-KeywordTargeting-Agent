import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from src.graph import build_keyword_agent

load_dotenv()

def main():
  api_key = os.getenv("GROQ_API_KEY")
  if not api_key:
    print("❌ خطا: لطفاً مقدار OPENAI_API_KEY را داخل فایل .env قرار دهید.")
    return

  print("⚙️ در حال راه‌اندازی مدل‌ها...")
  llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2)
  embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
  )

  agent = build_keyword_agent(llm, embedding_model)

  initial_input = {
    "domain": "site-saz.ir",
    "market": "طراحی سایت و فروشگاه‌سازهای ابری",
    "target_theme": "مقایسه سایت ساز با طراحی سایت اختصاصی و خرید فروشگاه ساز",
    "existing_pages": [
      {"title": "قیمت طراحی سایت اختصاصی", "url": "/custom-web-design-pricing"},
      {"title": "آموزش سئو سایت", "url": "/blog/seo-tutorial"}
    ],
    "raw_keywords": [
      "سایت ساز",
      "بهترین سایت ساز فروشگاهی",
      "طراحی سایت با کدنویسی یا وردپرس"
    ],
    "processed_keywords": [],
    "clusters": [],
    "briefs": [],
    "logs": []
  }

  config = {"configurable": {"thread_id": "session-run-1"}}

  print("🚀 اجرای پایپ‌لاین کیورد تارگتینگ در حال انجام است...\n")
  result = agent.invoke(initial_input, config=config)

  print("📋 === گزارش مراحل طی‌شده ===")
  for log in result.get("logs", []):
    print(f"✔️ {log}")

  print(f"\n📂 === خوشه‌های موضوعی شناسایی‌شده ({len(result.get('clusters', []))}) ===")
  for c in result.get("clusters", []):
    print(f"\n🏷️ کلاستر: {c.name}")
    print(f"   - نیت غالب: {c.dominant_intent} | امتیاز اولویت: {c.priority_score}")
    print(f"   - تصمیم معماری: {c.target_page}")
    if c.cannibalization_risk:
      print(f"   - ⚠️ خطر هم‌نوع‌خواری: {c.competing_pages}")
    print(f"   - کلمات کلیدی: {', '.join(c.keywords)}")

  print(f"\n📝 === بریف‌های محتوایی آماده تولید ({len(result.get('briefs', []))}) ===")
  for b in result.get("briefs", []):
    print(f"\n📌 بریف برای خوشه: {b.cluster_name} (نوع صفحه: {b.page_type})")
    print(f"   [تایتل سئو]: {b.seo_title}")
    print(f"   [تگ H1]: {b.h1}")
    print(f"   [متا دیسکریپشن]: {b.meta_description}")
    print(f"   [ساختار تیترها]: {' -> '.join(b.headings_structure)}")
    print("   [سوالات متداول FAQ]:")
    for faq in b.faqs:
      for q, a in faq.items():
        print(f"     ❓ {q}: {a}")

if __name__ == "__main__":
  main()