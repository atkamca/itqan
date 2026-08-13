with open('app/src/main/java/com/example/ui/theme/Type.kt', 'r') as f:
    code = f.read()

old = "val Quran_Font = FontFamily.Serif"
new = """val Quran_Font = FontFamily(
    Font(R.font.uthmanic_hafs, FontWeight.Normal)
)"""

code = code.replace(old, new)

if "androidx.compose.ui.text.font.Font" not in code:
    code = "import androidx.compose.ui.text.font.Font\n" + code
if "androidx.compose.ui.text.font.FontWeight" not in code:
    code = "import androidx.compose.ui.text.font.FontWeight\n" + code

with open('app/src/main/java/com/example/ui/theme/Type.kt', 'w') as f:
    f.write(code)

print("Type.kt updated.")
