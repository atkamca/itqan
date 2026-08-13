import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

import_sp = "import android.content.Context\nimport android.content.SharedPreferences\n"
if "import android.content.SharedPreferences" not in code:
    code = code.replace("import android.os.Bundle", import_sp + "import android.os.Bundle")

on_create_start = code.find("override fun onCreate")
on_create_end = code.find("CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {")

if on_create_start != -1 and on_create_end != -1:
    new_on_create = """override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val prefs = getSharedPreferences("crash_prefs", Context.MODE_PRIVATE)
        val lastCrash = prefs.getString("last_crash", null)
        prefs.edit().remove("last_crash").commit()
        
        Thread.setDefaultUncaughtExceptionHandler { _, e ->
            val stackTrace = android.util.Log.getStackTraceString(e)
            getSharedPreferences("crash_prefs", Context.MODE_PRIVATE).edit().putString("last_crash", stackTrace).commit()
            System.exit(1)
        }
        enableEdgeToEdge()
        setContent {
            if (lastCrash != null) {
                MaterialTheme {
                    androidx.compose.foundation.lazy.LazyColumn(Modifier.fillMaxSize().padding(16.dp)) {
                        item {
                            Text(lastCrash, color = Color.Red, fontSize = 12.sp, lineHeight = 16.sp)
                        }
                    }
                }
                return@setContent
            }
            """
    code = code[:on_create_start] + new_on_create + code[on_create_end:]

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
