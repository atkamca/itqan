import re

with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

code = code.replace("com.example.data.(searchQuery)", "searchQuery.normalizeQuranText()")
code = code.replace("com.example.data.(resultAyah.text)", "resultAyah.text.normalizeQuranText()")
code = code.replace("import com.example.data.QuranData\n", "import com.example.data.QuranData\nimport com.example.data.normalizeQuranText\n")

with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)

print("UI patched line 145.")
