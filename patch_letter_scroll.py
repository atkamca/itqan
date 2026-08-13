import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

# Replace FlowRow inside InteractiveLetterBox
# To be safe, I'll extract the code block and string replace.

old_block = """                    FlowRow(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        val options = when (showDialType) {
                            "madd" -> maddLetters.filter { it != charChunk }
                            "haraka" -> harakat.filter { !charChunk.contains(it) }
                            "letter" -> similarLetters
                            else -> emptyList()
                        }
                        options.forEach { opt ->
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

new_block = """                    val options = when (showDialType) {
                        "madd" -> maddLetters.filter { it != charChunk }
                        "haraka" -> harakat.filter { !charChunk.contains(it) }
                        "letter" -> similarLetters
                        else -> emptyList()
                    }
                    LazyColumn(
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

if old_block in code:
    code = code.replace(old_block, new_block)
    with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
        f.write(code)
    print("Replaced successfully")
else:
    print("Could not find old_block")
