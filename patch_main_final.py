import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

imports = """
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.material3.minimumInteractiveComponentSize
"""
code = code.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\n" + imports)

ayah_display_start = code.find("@OptIn(ExperimentalLayoutApi::class, ExperimentalFoundationApi::class)\n@Composable\nfun AyahDisplayView")

new_ayah = """@OptIn(ExperimentalLayoutApi::class, ExperimentalFoundationApi::class)
@Composable
fun AyahDisplayView(
    ayah: Ayah,
    isRevisionMode: Boolean,
    revealedWordsCount: Int,
    onRevealWord: (Int) -> Unit,
    errorLogs: List<ErrorLogEntity>,
    quranFont: androidx.compose.ui.text.font.FontFamily,
    viewModel: MainViewModel,
    onWordLongClick: (String) -> Unit
) {
    val words = ayah.text.split("\\\\s+".toRegex()).filter { it.isNotBlank() }
    
    FlowRow(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(4.dp, Alignment.CenterHorizontally),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        words.forEachIndexed { index, word ->
            val isRevealed = !isRevisionMode || index < revealedWordsCount
            
            val wordErrors = errorLogs.filter { it.surahId == ayah.surahId && it.ayahNumber == ayah.numberInSurah && it.wordText == word }
            val primaryError = wordErrors.minByOrNull { it.errorWeight } // Lower is worse
            
            val textColor = if (!isRevealed) MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)
                            else if (primaryError != null) getErrorColor(primaryError.errorType, MaterialTheme.colorScheme.onSurface)
                            else MaterialTheme.colorScheme.onSurface
                            
            val textDecoration = if (primaryError?.errorType?.contains("تشكيل") == true) TextDecoration.Underline else TextDecoration.None

            val bgColor = if (!isRevealed) MaterialTheme.colorScheme.surfaceVariant
                          else if (primaryError != null) getErrorColor(primaryError.errorType, Color.Transparent).copy(alpha = 0.15f)
                          else Color.Transparent

            val annotatedWord = if (!isRevealed) {
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
            }

            Box {
                Text(
                    text = annotatedWord,
                    fontSize = 32.sp,
                    lineHeight = 62.sp,
                    fontFamily = quranFont,
                    fontWeight = FontWeight.Normal,
                    textAlign = TextAlign.Center,
                    color = textColor,
                    textDecoration = textDecoration,
                    modifier = Modifier
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
                        .padding(horizontal = 4.dp, vertical = 2.dp)
                )
            }
        }
        
        val ayahErrors = errorLogs.filter { it.surahId == ayah.surahId && it.ayahNumber == ayah.numberInSurah && it.wordText == "[الآية]" }
        val hasAyahError = ayahErrors.isNotEmpty()
        
        val badgeColor = if (hasAyahError) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary
        
        Box(
            modifier = Modifier
                .minimumInteractiveComponentSize()
                .clip(RoundedCornerShape(16.dp))
                .clickable {
                    if (!isRevisionMode) {
                        onWordLongClick("[الآية]")
                    }
                }
                .padding(horizontal = 8.dp, vertical = 4.dp)
                .align(Alignment.CenterVertically),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "﴿${ayah.numberInSurah}﴾",
                fontSize = 32.sp,
                fontFamily = quranFont,
                color = badgeColor.copy(alpha = 0.8f)
            )
        }
    }
}
"""
code = code[:ayah_display_start] + new_ayah

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
