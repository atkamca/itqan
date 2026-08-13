import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

bad_fab = """ExtendedFloatingActionButton(
                    onClick = {
                        if (!isNextAyahVisible) {
                            isNextAyahVisible = true
                            revealedNextWordCount = 0
                        } else {
                            val nextAyahWords = nextAyah.text.split("\\\\s+".toRegex()).filter { it.isNotBlank() }
                            if (revealedNextWordCount < nextAyahWords.size) {
                                revealedNextWordCount++
                            } else {
                                coroutineScope.launch {
                                    pagerState.animateScrollToPage(pagerState.currentPage + 1)
                                }
                            }
                        }
                    },
                    icon = { Icon(Icons.Default.Visibility, contentDescription = null) },
                    text = { Text("الآية الموالية") },
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
                    modifier = Modifier.combinedClickable("""

good_fab = """ExtendedFloatingActionButton(
                    onClick = { /* Handled by combinedClickable below */ },
                    icon = { Icon(Icons.Default.Visibility, contentDescription = null) },
                    text = { Text("الآية الموالية") },
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
                    modifier = Modifier.combinedClickable("""

code = code.replace(bad_fab, good_fab)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
