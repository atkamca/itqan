with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

code = code.replace("import com.example.data.normalizeQuranText\npackage com.example.ui\n", "package com.example.ui\nimport com.example.data.normalizeQuranText\n")

with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)

print("Imports fixed.")
