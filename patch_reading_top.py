import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

old_topbar = """TopAppBar(
                title = {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        SurahDropdown(
                            selectedSurahId = selectedSurahId,
                            onSurahSelected = { viewModel.selectSurah(it) }
                        )
                        if (currentAyah != null) {
                            TextButton(onClick = { showJumpDialog = true }) {
                                Text(
                                    text = "آية ${currentAyah.numberInSurah}",
                                    fontSize = 18.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                },
                actions = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(if (isRevisionMode) "تلاوة" else "تحليل", modifier = Modifier.padding(end = 8.dp))
                        Switch(
                            checked = isRevisionMode,
                            onCheckedChange = { isRevisionMode = it }
                        )
                    }
                }
            )"""

new_topbar = """TopAppBar(
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background.copy(alpha = 0.9f),
                    titleContentColor = MaterialTheme.colorScheme.primary,
                ),
                title = {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(end = 8.dp),
                        horizontalArrangement = Arrangement.Start,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        SurahDropdown(
                            selectedSurahId = selectedSurahId,
                            onSurahSelected = { viewModel.selectSurah(it) }
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        if (currentAyah != null) {
                            TextButton(
                                onClick = { showJumpDialog = true },
                                modifier = Modifier.clip(RoundedCornerShape(12.dp)),
                                colors = ButtonDefaults.textButtonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                            ) {
                                Text(
                                    text = "آية ${currentAyah.numberInSurah}",
                                    fontSize = 16.sp,
                                    fontFamily = com.example.ui.theme.UI_Font,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                },
                actions = {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .padding(end = 16.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text(
                            text = if (isRevisionMode) "تلاوة" else "تحليل", 
                            fontFamily = com.example.ui.theme.UI_Font,
                            fontWeight = FontWeight.Medium,
                            fontSize = 14.sp,
                            modifier = Modifier.padding(end = 8.dp)
                        )
                        Switch(
                            checked = isRevisionMode,
                            onCheckedChange = { isRevisionMode = it },
                            modifier = Modifier.scale(0.8f)
                        )
                    }
                }
            )"""

code = code.replace(old_topbar, new_topbar)

# Fix SurahDropdown font
old_dropdown = """Text(
            text = selectedSurah?.name ?: "السورة",
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )"""
new_dropdown = """Text(
            text = selectedSurah?.name ?: "السورة",
            fontSize = 22.sp,
            fontFamily = com.example.ui.theme.UI_Font,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )"""
code = code.replace(old_dropdown, new_dropdown)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)

print("Updated ReadingScreen TopAppBar")
