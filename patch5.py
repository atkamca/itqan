import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

cleanup_str = """        val prefs = getSharedPreferences("crash_prefs", Context.MODE_PRIVATE)
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
            }"""

clean_str = """        enableEdgeToEdge()
        setContent {"""

code = code.replace(cleanup_str, clean_str)

import_str = "import android.content.Context\nimport android.content.SharedPreferences\n"
code = code.replace(import_str, "")

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
