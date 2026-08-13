import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# Let's fix Scaffold inside ReadingScreen
start_scaffold_idx = code.find("    Scaffold(\n        containerColor =")
if start_scaffold_idx != -1:
    end_scaffold_idx = code.find("    ) { paddingValues ->", start_scaffold_idx)
    code = code[:start_scaffold_idx] + "    Scaffold(\n        containerColor = MaterialTheme.colorScheme.background\n" + code[end_scaffold_idx:]

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
