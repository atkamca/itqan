with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

if "import com.example.data.normalizeQuranText" not in code:
    code = "import com.example.data.normalizeQuranText\n" + code

with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)

print("Imports updated.")
