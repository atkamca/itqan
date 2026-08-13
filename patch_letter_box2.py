import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

start_idx = code.find("@OptIn(ExperimentalLayoutApi::class)\n@Composable\nfun InteractiveLetterBox(")
interactive_box_code = """@OptIn(ExperimentalLayoutApi::class)
@Composable
fun InteractiveLetterBox(
    charChunk: String,
    onDiacriticChange: (String) -> Unit,
    onDelete: () -> Unit,
    onReplaceLetter: (String) -> Unit
) {
    var offsetX by remember { mutableFloatStateOf(0f) }
    var offsetY by remember { mutableFloatStateOf(0f) }
    var showDialType by remember { mutableStateOf<String?>(null) } // "madd", "haraka", "letter"
    var isDeleted by remember { mutableStateOf(false) }

    val alpha by animateFloatAsState(targetValue = if (isDeleted) 0.3f else 1f, label = "alpha")

    val isMadd = charChunk.length == 1 && charChunk in listOf("ا", "و", "ي", "ى")
    val maddLetters = listOf("ا", "و", "ي", "ى")
    val harakat = listOf("َ", "ُ", "ِ", "ْ", "ّ", "ً", "ٌ", "ٍ", "َّ", "ُّ", "ِّ")
    val similarLetters = listOf("س", "ص", "ض", "ظ", "ذ", "ز", "ت", "ط", "ق", "ك", "ح", "خ", "ه", "ء", "ا", "و", "ي") 

    Box(contentAlignment = Alignment.Center) {
        if (showDialType != null) {
            androidx.compose.ui.window.Popup(
                alignment = Alignment.TopCenter,
                offset = IntOffset(0, if (showDialType == "letter") 180 else -180),
                onDismissRequest = { showDialType = null },
                properties = androidx.compose.ui.window.PopupProperties(focusable = true, dismissOnClickOutside = true)
            ) {
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.primaryContainer)
                        .padding(12.dp)
                        .widthIn(max = 280.dp)
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
        }

        Box(
            modifier = Modifier
                .offset { IntOffset(offsetX.roundToInt(), offsetY.roundToInt()) }
                .padding(4.dp)
                .clip(RoundedCornerShape(8.dp))
                .background(if (isDeleted) MaterialTheme.colorScheme.surfaceVariant else MaterialTheme.colorScheme.secondaryContainer)
                .pointerInput(Unit) {
                    detectDragGestures(
                        onDragEnd = {
                            if (offsetX > 100f || offsetX < -100f) {
                                isDeleted = true
                                onDelete()
                            } else if (offsetY < -50f) { // Swipe Up
                                if (isMadd) showDialType = "madd" else showDialType = "haraka"
                                offsetY = 0f
                                offsetX = 0f
                            } else if (offsetY > 50f && !isMadd) { // Swipe Down
                                showDialType = "letter"
                                offsetY = 0f
                                offsetX = 0f
                            } else {
                                offsetX = 0f
                                offsetY = 0f
                                showDialType = null
                            }
                        }
                    ) { change, dragAmount ->
                        change.consume()
                        offsetX += dragAmount.x
                        offsetY += dragAmount.y
                    }
                }
                .padding(16.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = charChunk, 
                fontFamily = Quran_Font, 
                fontSize = 32.sp, 
                color = MaterialTheme.colorScheme.onSecondaryContainer.copy(alpha = alpha)
            )
        }
    }
}
"""

if start_idx != -1:
    code = code[:start_idx] + interactive_box_code
    with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
        f.write(code)
    print("Replaced!")
else:
    print("Not found!")
