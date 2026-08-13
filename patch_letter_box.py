import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

# Replace the inner Box dial with Popup
dial_box_regex = r"if \(showDialType != null\) \{.*?FlowRow\(.*?\}\s*\}\s*\}"
dial_box_replacement = """if (showDialType != null) {
            androidx.compose.ui.window.Popup(
                alignment = androidx.compose.ui.Alignment.TopCenter,
                offset = IntOffset(0, if (showDialType == "letter") 150 else -150),
                onDismissRequest = { showDialType = null },
                properties = androidx.compose.ui.window.PopupProperties(focusable = true, dismissOnClickOutside = true)
            ) {
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.primaryContainer)
                        .padding(12.dp)
                        .widthIn(max = 250.dp)
                ) {
                    FlowRow(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
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
                    }
                }
            }
        }"""
        
# Note: the regex needs to be extremely precise because we're matching nested braces. It's safer to just split and replace.
