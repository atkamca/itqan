import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# Add blur import if not there
if "import androidx.compose.ui.draw.blur" not in code:
    code = code.replace("import androidx.compose.ui.draw.clip", "import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.draw.blur\nimport androidx.compose.ui.input.pointer.PointerEventPass")

# 1. Update FAB Next Ayah onClick logic (to just show the next ayah if not visible, words logic is fine)
# The prompt says: "عند الضغط على الزر، قم بتحديث القائمة المعروضة فوراً لإضافة أجزاء الآية التالية بحالة محجوبة بالكامل (Blur Effect)."
# The current logic is:
# if (!isNextAyahVisible) { isNextAyahVisible = true; revealedNextWordCount = 0 }
# This is exactly what we want. We just need to change how !isRevealed is rendered.

# 2. Update AyahDisplayView rendering and add microSwipeGesture
ayah_display_old = """            val annotatedWord = if (!isRevealed) {
                buildAnnotatedString { append("••••") }
            } else {
                buildAnnotatedString {
                    val errorChars = wordErrors.mapNotNull { it.charIndex }
                    word.forEachIndexed { i, c ->
                        if (i in errorChars) {
                            withStyle(SpanStyle(color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Black, textDecoration = TextDecoration.Underline)) { append(c.toString()) }
                        } else {
                            append(c.toString())
                        }
                    }
                }
            }"""

ayah_display_new = """            val annotatedWord = buildAnnotatedString {
                val errorChars = wordErrors.mapNotNull { it.charIndex }
                word.forEachIndexed { i, c ->
                    if (i in errorChars) {
                        withStyle(SpanStyle(color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Black, textDecoration = TextDecoration.Underline)) { append(c.toString()) }
                    } else {
                        append(c.toString())
                    }
                }
            }
            
            val blurRadius = if (!isRevealed) 12.dp else 0.dp"""

code = code.replace(ayah_display_old, ayah_display_new)

# Update Text modifier to use blur and microSwipe
text_modifier_old = """                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(bgColor)
                        .pointerInput(isRevealed, isRevisionMode) {
                            detectTapGestures(
                                onTap = {
                                    if (isRevisionMode) {
                                        if (!isRevealed) {
                                            onRevealWord(index + 1)
                                        } else {
                                            // Single tap on revealed word logs hesitation (Yellow)
                                            viewModel.logError(ayah, word, "تردد / توقف سريع")
                                        }
                                    }
                                },
                                onDoubleTap = {
                                    if (isRevisionMode && isRevealed) {
                                        // Double tap logs forgotten word (Red)
                                        viewModel.logError(ayah, word, "توقف تام ونسيان الكلمة")
                                    }
                                },
                                onLongPress = {
                                    if (!isRevisionMode && isRevealed) {
                                        onWordLongClick(word)
                                    }
                                }
                            )
                        }
                        .padding(horizontal = 4.dp, vertical = 2.dp)"""

text_modifier_new = """                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(bgColor)
                        .blur(blurRadius)
                        .pointerInput(isRevealed, isRevisionMode) {
                            awaitPointerEventScope {
                                while (true) {
                                    val downEvent = awaitPointerEvent(PointerEventPass.Initial)
                                    if (!downEvent.changes.first().pressed) continue
                                    val startY = downEvent.changes.first().position.y
                                    var isConsumed = false
                                    
                                    while (true) {
                                        val moveEvent = awaitPointerEvent(PointerEventPass.Initial)
                                        val change = moveEvent.changes.firstOrNull() ?: break
                                        if (!change.pressed) {
                                            // on tap detection
                                            if (!isConsumed) {
                                                // We can rely on a separate tap detector, but since we use PointerEventPass.Initial
                                                // it might interfere. Actually, let's keep detectTapGestures in a separate block
                                                // and only consume here IF it's a swipe.
                                            }
                                            break
                                        }
                                        
                                        if (!isConsumed) {
                                            val deltaY = change.position.y - startY
                                            if (deltaY < -40f) { // Swipe Up
                                                if (isRevisionMode && isRevealed) {
                                                    viewModel.logError(ayah, word, "تردد / توقف سريع")
                                                }
                                                isConsumed = true
                                                change.consume()
                                            } else if (deltaY > 40f) { // Swipe Down
                                                if (isRevisionMode && isRevealed) {
                                                    viewModel.logError(ayah, word, "توقف تام ونسيان الكلمة")
                                                }
                                                isConsumed = true
                                                change.consume()
                                            }
                                        } else {
                                            change.consume()
                                        }
                                    }
                                }
                            }
                        }
                        .pointerInput(isRevealed, isRevisionMode) {
                            detectTapGestures(
                                onTap = {
                                    if (isRevisionMode) {
                                        if (!isRevealed) {
                                            onRevealWord(index + 1)
                                        }
                                    }
                                },
                                onLongPress = {
                                    if (!isRevisionMode && isRevealed) {
                                        onWordLongClick(word)
                                    }
                                }
                            )
                        }
                        .padding(horizontal = 4.dp, vertical = 2.dp)"""

code = code.replace(text_modifier_old, text_modifier_new)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
