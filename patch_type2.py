with open('app/src/main/java/com/example/ui/theme/Type.kt', 'r') as f:
    code = f.read()

old = """val Quran_Font = FontFamily(
    Font(R.font.amiri_regular, FontWeight.Normal)
)"""
new = "val Quran_Font = FontFamily.Serif"

code = code.replace(old, new)
with open('app/src/main/java/com/example/ui/theme/Type.kt', 'w') as f:
    f.write(code)
