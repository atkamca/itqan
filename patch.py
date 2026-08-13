import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

imports = """
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateOf
"""
code = code.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\n' + imports)

class_start = "class MainActivity : ComponentActivity() {"
new_class = """class MainActivity : ComponentActivity() {
    private var crashMessage by mutableStateOf<String?>(null)
"""
code = code.replace(class_start, new_class)

on_create = """override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Thread.setDefaultUncaughtExceptionHandler { _, e ->
            val stackTrace = android.util.Log.getStackTraceString(e)
            android.os.Handler(android.os.Looper.getMainLooper()).post {
                crashMessage = stackTrace
            }
        }
        enableEdgeToEdge()
        setContent {
            if (crashMessage != null) {
                MaterialTheme {
                    androidx.compose.foundation.lazy.LazyColumn(Modifier.fillMaxSize().padding(16.dp)) {
                        item {
                            Text(crashMessage ?: "", color = Color.Red, fontSize = 12.sp, lineHeight = 16.sp)
                        }
                    }
                }
                return@setContent
            }
"""
code = code.replace("""override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {""", on_create)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
