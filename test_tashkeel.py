import re

def removeTashkeel(text):
    # Expanded regex to include Quranic signs
    return re.sub(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]', '', text)

print(removeTashkeel("ٱلرَّحْمَٰنِ"))
print(removeTashkeel("بِسْمِ ٱللَّهِ"))
