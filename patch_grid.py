import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

old_list = """                    LazyColumn(
                        modifier = Modifier.heightIn(max = 240.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        items(options) { opt ->
                            Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surface)
                                    .clickable {
                                        showDialType = null
                                        if (options == harakat) onDiacriticChange(opt)
                                        else onReplaceLetter(opt)
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text(text = if (showDialType == "haraka") "ـ$opt" else opt, fontSize = 28.sp, color = MaterialTheme.colorScheme.onSurface)
                            }
                        }
                    }"""

new_list = """                    androidx.compose.foundation.lazy.grid.LazyVerticalGrid(
                        columns = androidx.compose.foundation.lazy.grid.GridCells.Adaptive(minSize = 48.dp),
                        modifier = Modifier.heightIn(max = 240.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        androidx.compose.foundation.lazy.grid.items(options) { opt ->
                            Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surface)
                                    .clickable {
                                        showDialType = null
                                        if (options == harakat) onDiacriticChange(opt)
                                        else onReplaceLetter(opt)
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text(text = if (showDialType == "haraka") "ـ$opt" else opt, fontSize = 28.sp, color = MaterialTheme.colorScheme.onSurface)
                            }
                        }
                    }"""

code = code.replace(old_list, new_list)

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)
print("Replaced grid successfully")
