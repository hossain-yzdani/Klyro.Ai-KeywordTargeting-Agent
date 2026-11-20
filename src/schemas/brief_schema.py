from typing import List, Dict
from pydantic import BaseModel, Field

class SingleBriefOutput(BaseModel):
  cluster_name: str = Field(description="نام خوشه موضوعی")
  page_type: str = Field(description="نوع صفحه: Pillar یا Cluster")
  seo_title: str = Field(description="تایتل سئو جذاب با رعایت طول استاندارد (زیر ۶۰ کاراکتر)")
  h1: str = Field(description="هدینگ اصلی صفحه")
  meta_description: str = Field(description="توضیحات متا جذاب با کال تو اکشن (زیر ۱۵۵ کاراکتر)")
  headings_structure: List[str] = Field(description="ساختار پیشنهادی تگ‌های H2 و H3 به ترتیب منطقی")
  faqs: List[Dict[str, str]] = Field(description="حداقل ۳ سوال متداول به همراه پاسخ کوتاه در قالب key-value")
  internal_linking_suggestions: List[str] = Field(description="پیشنهاد موضوعات یا صفحات برای لینک‌سازی داخلی")