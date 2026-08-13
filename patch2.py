import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

bad_set_content = """        setContent {
            if (crashMessage != null) {
                MaterialTheme {
                    androidx.compose.foundation.lazy.LazyColumn(Modifier.fillMaxSize().padding(16.dp)) {
                        item {
                            Text(crashMessage ?: "", color = Color.Red, fontSize = 12.sp, lineHeight = 16.sp)
                        }
                    }
                }
                return@setContent
            }"""

good_set_content = """        setContent {
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
            }"""

code = code.replace(bad_set_content, good_set_content)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
