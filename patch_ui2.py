with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

code = code.replace("com.example.data.(word)", "word.normalizeQuranText()")
code = code.replace("QuranData.normalizeArabic(word)", "word.normalizeQuranText()")

with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)

print("UI patched again.")
