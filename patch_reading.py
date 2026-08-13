import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# 1. Remove floatingActionButton entirely
fab_pattern = r"floatingActionButton = \{.*?\},\s*containerColor"
code = re.sub(fab_pattern, "containerColor", code, flags=re.DOTALL)

# 2. Remove states
code = code.replace("    // New states for Next Ayah\n    var isNextAyahVisible by remember { mutableStateOf(false) }\n    var revealedNextWordCount by remember { mutableIntStateOf(0) }", "")
code = code.replace("        isNextAyahVisible = false\n        revealedNextWordCount = 0", "")

# 3. Remove next ayah block at the bottom of the page
next_ayah_pattern = r"// Next Ayah Preview.*?AnimatedVisibility.*?\}\s*\}"
code = re.sub(next_ayah_pattern, "", code, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
