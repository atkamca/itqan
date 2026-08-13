import re

with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

old_box = """Box(
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
                            }"""

new_box = """Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surface)
                                    .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.5f), CircleShape)
                                    .clickable {
                                        showDialType = null
                                        if (options == harakat) onDiacriticChange(opt)
                                        else onReplaceLetter(opt)
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = if (showDialType == "haraka") "ـ$opt" else opt, 
                                    fontSize = 24.sp, 
                                    color = MaterialTheme.colorScheme.primary,
                                    fontFamily = com.example.ui.theme.Quran_Font
                                )
                            }"""

code = code.replace(old_box, new_box)

with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)

print("Updated Analysis Chips")
