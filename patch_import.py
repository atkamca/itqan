with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

import_statement = "import androidx.compose.foundation.lazy.grid.items\n"
if "import androidx.compose.foundation.lazy.grid.items" not in code:
    code = code.replace("import androidx.compose.foundation.lazy.items\n", "import androidx.compose.foundation.lazy.items\n" + import_statement)
    with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
        f.write(code)
    print("Import added")
