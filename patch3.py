import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

bad_on_create = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Thread.setDefaultUncaughtExceptionHandler { _, e ->
            val stackTrace = android.util.Log.getStackTraceString(e)
            android.os.Handler(android.os.Looper.getMainLooper()).post {
                crashMessage = stackTrace
            }
        }
        enableEdgeToEdge()
        setContent {
            val crash = crashMessage
            if (crash != null) {
                MaterialTheme {
                    androidx.compose.foundation.lazy.LazyColumn(Modifier.fillMaxSize().padding(16.dp)) {
                        item {
                            Text(crash ?: "", color = Color.Red, fontSize = 12.sp, lineHeight = 16.sp)
                        }
                    }
                }
                return@setContent
            }
            CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {"""

good_on_create = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val prefs = getSharedPreferences("crash_prefs", android.content.Context.MODE_PRIVATE)
        val lastCrash = prefs.getString("last_crash", null)
        prefs.edit().remove("last_crash").apply() // clear it
        
        Thread.setDefaultUncaughtExceptionHandler { _, e ->
            val stackTrace = android.util.Log.getStackTraceString(e)
            prefs.edit().putString("last_crash", stackTrace).commit()
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
            CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {"""

code = code.replace(bad_on_create, good_on_create)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
