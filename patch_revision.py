with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

code = code.replace("var isRevisionMode by remember { mutableStateOf(true) }", "var isRevisionMode by remember { mutableStateOf(false) }")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)

print("isRevisionMode updated.")
