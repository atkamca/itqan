import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

missing_composables = """
@Composable
fun SurahDropdown(selectedSurahId: Int, onSurahSelected: (Int) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    val surahs = com.example.data.QuranData.surahs
    val selectedSurah = surahs.find { it.id == selectedSurahId }
    
    Box {
        TextButton(onClick = { expanded = true }) {
            Text(
                text = selectedSurah?.name ?: "السورة",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )
        }
        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false },
            modifier = Modifier.heightIn(max = 300.dp)
        ) {
            surahs.forEach { surah ->
                DropdownMenuItem(
                    text = { Text(surah.name) },
                    onClick = {
                        onSurahSelected(surah.id)
                        expanded = false
                    }
                )
            }
        }
    }
}

@Composable
fun AyahJumpDialog(currentAyah: Int, onDismiss: () -> Unit, onJump: (Int) -> Unit) {
    var text by remember { mutableStateOf(currentAyah.toString()) }
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("الانتقال لآية") },
        text = {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it.filter { char -> char.isDigit() } },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
        },
        confirmButton = {
            TextButton(onClick = {
                text.toIntOrNull()?.let { onJump(it) }
            }) {
                Text("انتقال")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("إلغاء")
            }
        }
    )
}
"""

if "fun SurahDropdown" not in code:
    code = code.replace("@Composable\nfun ReportsScreen", missing_composables + "\n@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ReportsScreen")

code = code.replace("Modifier.com.example.ui.swipeWatcher", "Modifier.swipeWatcher")
code = code.replace("import com.example.ui.MainViewModel", "import com.example.ui.MainViewModel\nimport com.example.ui.swipeWatcher")

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
