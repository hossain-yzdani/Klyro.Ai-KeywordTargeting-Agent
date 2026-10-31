import re

def clean_persian_text(text: str) -> str:
    """
    استانداردسازی رسم‌الخط فارسی و حذف کاراکترهای زائد:
    - تبدیل ي و ك عربی به ی و ک فارسی
    - حذف علائم نگارشی متداول
    - استانداردسازی نیم‌فاصله و فاصله‌های اضافه
    """
    if not text:
        return ""

    text = text.replace("ي", "ی").replace("ك", "ک")
    
    text = re.sub(r'[\u200c\s]+', ' ', text)
    
    text = re.sub(r'[!؟?\\.,:;"\'()\[\]{}]+', '', text)
    
    return text.strip().lower()