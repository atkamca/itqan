import re

def removeTashkeel(text):
    return re.sub(r'[\u0617-\u061A\u064B-\u0652\u0670]', '', text)

def normalizeArabic(text):
    text = removeTashkeel(text)
    text = re.sub(r'[أإآٱ]', 'ا', text)
    text = text.replace("ة", "ه")
    text = text.replace("ى", "ي")
    text = text.replace("ؤ", "و")
    text = text.replace("ئ", "ي")
    return text

text = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
query = "ٱلرَّحْمَٰنِ"
print("Text:", normalizeArabic(text))
print("Query:", normalizeArabic(query))
