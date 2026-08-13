import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# Replace SurahDropdown
surah_old = """@Composable
fun SurahDropdown(selectedSurahId: Int, onSurahSelected: (Int) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    val surahs = com.example.data.QuranData.surahs
    val selectedSurah = surahs.find { it.id == selectedSurahId }
    
    Box {
        TextButton(onClick = { expanded = true }) {
            Text(
                text = selectedSurah?.name ?: "السورة",
                fontSize = 20.sp,
                fontWeight = androidx.compose.ui.text.font.FontWeight.Bold
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
}"""

surah_new = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SurahDropdown(selectedSurahId: Int, onSurahSelected: (Int) -> Unit) {
    var showSheet by remember { mutableStateOf(false) }
    val surahs = com.example.data.QuranData.surahs
    val selectedSurah = surahs.find { it.id == selectedSurahId }
    
    TextButton(onClick = { showSheet = true }, modifier = Modifier.clip(RoundedCornerShape(8.dp))) {
        Text(
            text = selectedSurah?.name ?: "السورة",
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
    }

    if (showSheet) {
        ModalBottomSheet(onDismissRequest = { showSheet = false }) {
            Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)) {
                Text("اختر السورة", fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))
                LazyColumn(modifier = Modifier.fillMaxWidth()) {
                    items(surahs) { surah ->
                        val isSelected = surah.id == selectedSurahId
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .background(if (isSelected) MaterialTheme.colorScheme.primaryContainer else Color.Transparent)
                                .clickable {
                                    onSurahSelected(surah.id)
                                    showSheet = false
                                }
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(surah.name, fontSize = 18.sp, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal, color = if(isSelected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface)
                            Text("${surah.ayahCount} آية", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
    }
}"""

# Replace AyahJumpDialog
ayah_old = """@Composable
fun AyahJumpDialog(currentAyah: Int, onDismiss: () -> Unit, onJump: (Int) -> Unit) {
    var text by remember { mutableStateOf(currentAyah.toString()) }
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("الانتقال لآية") },
        text = {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it.filter { char -> char.isDigit() } },
                keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number)
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
}"""

ayah_new = """@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun AyahJumpDialog(currentAyah: Int, totalAyahs: Int, onDismiss: () -> Unit, onJump: (Int) -> Unit) {
    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)) {
            Text("الانتقال إلى آية", fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))
            
            LazyColumn(modifier = Modifier.fillMaxWidth().weight(1f, fill = false)) {
                item {
                    FlowRow(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        for (i in 1..totalAyahs) {
                            val isSelected = i == currentAyah
                            Box(
                                modifier = Modifier
                                    .size(60.dp)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)
                                    .clickable { onJump(i) },
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = i.toString(),
                                    fontSize = 18.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}"""

code = code.replace(surah_old, surah_new)
code = code.replace(ayah_old, ayah_new)

# Wait, AyahJumpDialog call in ReadingScreen must pass totalAyahs!
# Let's fix that too.
call_old = """            if (showJumpDialog) {
                AyahJumpDialog(
                    currentAyah = currentAyah?.numberInSurah ?: 1,
                    onDismiss = { showJumpDialog = false },
                    onJump = { ayahNum ->
                        viewModel.jumpToAyah(ayahNum)
                        showJumpDialog = false
                    }
                )
            }"""

call_new = """            if (showJumpDialog) {
                val totalAyahs = com.example.data.QuranData.surahs.find { it.id == selectedSurahId }?.ayahCount ?: 1
                AyahJumpDialog(
                    currentAyah = currentAyah?.numberInSurah ?: 1,
                    totalAyahs = totalAyahs,
                    onDismiss = { showJumpDialog = false },
                    onJump = { ayahNum ->
                        viewModel.jumpToAyah(ayahNum)
                        showJumpDialog = false
                    }
                )
            }"""

code = code.replace(call_old, call_new)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
