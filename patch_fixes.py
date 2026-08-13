import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# Fix 1: AutoMirrored.Filled.MenuBook -> Filled.MenuBook
code = code.replace("Icons.AutoMirrored.Filled.MenuBook", "Icons.Filled.MenuBook")

# Fix 2: Import animation and fix syntax
if "import androidx.compose.animation.*" not in code:
    code = code.replace("import androidx.compose.foundation.background", "import androidx.compose.foundation.background\nimport androidx.compose.animation.*")

code = code.replace(
    "androidx.compose.animation.fadeIn() androidx.compose.animation.togetherWith androidx.compose.animation.fadeOut()",
    "androidx.compose.animation.fadeIn() togetherWith androidx.compose.animation.fadeOut()"
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)


with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code2 = f.read()

if "import androidx.compose.foundation.border" not in code2:
    code2 = code2.replace("import androidx.compose.foundation.background", "import androidx.compose.foundation.background\nimport androidx.compose.foundation.border")

with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code2)

print("Fixes applied")
