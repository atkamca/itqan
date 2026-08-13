import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

if "import androidx.compose.ui.draw.scale" not in code:
    code = code.replace("import androidx.compose.ui.draw.clip", "import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.draw.scale")

if "import androidx.compose.material3.TopAppBarDefaults" not in code:
    code = code.replace("import androidx.compose.material3.*", "import androidx.compose.material3.*\nimport androidx.compose.material3.TopAppBarDefaults")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
