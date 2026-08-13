import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# 1. Remove FAB completely
fab_regex = r"floatingActionButton = \{.*?\},\\s*floatingActionButtonPosition = FabPosition\.Center"
code = re.sub(fab_regex, "", code, flags=re.DOTALL)

# 2. Update pointerInput blocks to remove `isRevisionMode` condition for tap/gestures
# The first pointerInput (swipe up/down)
swipe_old = """                                            if (deltaY < -40f) { // Swipe Up
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
                                            }"""

swipe_new = """                                            if (deltaY < -40f) { // Swipe Up
                                                if (isRevealed) {
                                                    viewModel.logError(ayah, word, "تردد / توقف سريع")
                                                }
                                                isConsumed = true
                                                change.consume()
                                            } else if (deltaY > 40f) { // Swipe Down
                                                if (isRevealed) {
                                                    viewModel.logError(ayah, word, "توقف تام ونسيان الكلمة")
                                                }
                                                isConsumed = true
                                                change.consume()
                                            }"""
code = code.replace(swipe_old, swipe_new)

# The second pointerInput (tap/long press)
tap_old = """                            detectTapGestures(
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
                            )"""

tap_new = """                            detectTapGestures(
                                onTap = {
                                    if (!isRevealed) {
                                        onRevealWord(index + 1)
                                    }
                                },
                                onLongPress = {
                                    if (isRevealed) {
                                        onWordLongClick(word)
                                    }
                                }
                            )"""
code = code.replace(tap_old, tap_new)

# 3. Update the Box for Ayah number
ayah_box_old = """                .clickable {
                    if (!isRevisionMode) {
                        onWordLongClick("[الآية]")
                    }
                }"""
ayah_box_new = """                .clickable {
                    onWordLongClick("[الآية]")
                }"""
code = code.replace(ayah_box_old, ayah_box_new)

# Also remove the nextAyah display completely since there's no FAB
next_ayah_display = r"if \(page == pagerState\.currentPage && isNextAyahVisible && nextAyah != null\) \{.*?\}\n"
code = re.sub(next_ayah_display, "", code, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
