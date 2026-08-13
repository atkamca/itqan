import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

reading_screen_start = code.find("@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class, ExperimentalLayoutApi::class)\n@Composable\nfun ReadingScreen")
if reading_screen_start == -1:
    print("Could not find ReadingScreen")
    exit(1)

reading_screen_end = code.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ReportsScreen", reading_screen_start)
if reading_screen_end == -1:
    print("Could not find end of ReadingScreen")
    exit(1)

new_reading_screen = """@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class, ExperimentalLayoutApi::class)
@Composable
fun ReadingScreen(viewModel: MainViewModel) {
    val currentAyahs by viewModel.currentAyahs.collectAsStateWithLifecycle()
    val errorLogs by viewModel.errorLogs.collectAsStateWithLifecycle()
    val selectedSurahId by viewModel.selectedSurahId.collectAsStateWithLifecycle()
    val jumpIndex by viewModel.jumpToAyahIndex.collectAsStateWithLifecycle()
    
    val pagerState = rememberPagerState(pageCount = { currentAyahs.size })
    val coroutineScope = rememberCoroutineScope()
    
    var isRevisionMode by remember { mutableStateOf(false) }
    var revealedWordsCount by remember { mutableIntStateOf(0) }
    
    // New states for Next Ayah
    var isNextAyahVisible by remember { mutableStateOf(false) }
    var revealedNextWordCount by remember { mutableIntStateOf(0) }
    
    LaunchedEffect(jumpIndex) {
        if (jumpIndex != -1 && jumpIndex < currentAyahs.size) {
            pagerState.scrollToPage(jumpIndex)
            viewModel.resetJumpIndex()
        }
    }

    LaunchedEffect(pagerState.currentPage, isRevisionMode) {
        revealedWordsCount = 0
        isNextAyahVisible = false
        revealedNextWordCount = 0
    }

    var selectedWordForAnalysis by remember { mutableStateOf<Pair<Ayah, String>?>(null) }
    var showJumpDialog by remember { mutableStateOf(false) }
    
    val currentAyah = currentAyahs.getOrNull(pagerState.currentPage)
    val nextAyah = currentAyahs.getOrNull(pagerState.currentPage + 1)
    
    if (selectedWordForAnalysis != null) {
        com.example.ui.WordAnalysisBottomSheet(
            word = selectedWordForAnalysis!!.second,
            ayah = selectedWordForAnalysis!!.first,
            viewModel = viewModel,
            onDismissRequest = { selectedWordForAnalysis = null }
        )
    }

    Scaffold(
        floatingActionButton = {
            if (nextAyah != null) {
                ExtendedFloatingActionButton(
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
                    modifier = Modifier.com.example.ui.swipeWatcher(
                        onSwipeUp = {
                            val nextAyahWords = nextAyah.text.split("\\\\s+".toRegex()).filter { it.isNotBlank() }
                            revealedNextWordCount = nextAyahWords.size
                        },
                        onSwipeDown = {
                            val nextAyahWords = nextAyah.text.split("\\\\s+".toRegex()).filter { it.isNotBlank() }
                            revealedNextWordCount = nextAyahWords.size
                        }
                    )
                )
            }
        },
        floatingActionButtonPosition = FabPosition.Center
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(bottom = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            TopAppBar(
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
                        Text("مراجعة", modifier = Modifier.padding(end = 8.dp))
                        Switch(
                            checked = isRevisionMode,
                            onCheckedChange = { isRevisionMode = it }
                        )
                    }
                }
            )

            if (showJumpDialog) {
                AyahJumpDialog(
                    currentAyah = currentAyah?.numberInSurah ?: 1,
                    onDismiss = { showJumpDialog = false },
                    onJump = { ayahNum ->
                        viewModel.jumpToAyah(ayahNum)
                        showJumpDialog = false
                    }
                )
            }

            if (currentAyahs.isEmpty()) return@Column

            val quranFont = com.example.ui.theme.Quran_Font
            
            HorizontalPager(
                state = pagerState,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth(),
            ) { page ->
                val ayah = currentAyahs[page]
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(horizontal = 24.dp, vertical = 16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .verticalScroll(rememberScrollState())
                            .padding(bottom = 80.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        AyahDisplayView(
                            ayah = ayah,
                            isRevisionMode = isRevisionMode,
                            revealedWordsCount = revealedWordsCount,
                            errorLogs = errorLogs,
                            quranFont = quranFont,
                            viewModel = viewModel,
                            onWordLongClick = { w -> selectedWordForAnalysis = Pair(ayah, w) },
                            onAyahLongClick = { /* Mutashabihat for Ayah */ }
                        )
                        
                        if (page == pagerState.currentPage && isNextAyahVisible && nextAyah != null) {
                            Spacer(modifier = Modifier.height(32.dp))
                            Divider(modifier = Modifier.padding(horizontal = 32.dp))
                            Spacer(modifier = Modifier.height(32.dp))
                            AyahDisplayView(
                                ayah = nextAyah,
                                isRevisionMode = true,
                                revealedWordsCount = revealedNextWordCount,
                                errorLogs = errorLogs,
                                quranFont = quranFont,
                                viewModel = viewModel,
                                onWordLongClick = { w -> selectedWordForAnalysis = Pair(nextAyah, w) },
                                onAyahLongClick = { /* Mutashabihat for Ayah */ }
                            )
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class, ExperimentalFoundationApi::class)
@Composable
fun AyahDisplayView(
    ayah: Ayah,
    isRevisionMode: Boolean,
    revealedWordsCount: Int,
    errorLogs: List<ErrorLogEntity>,
    quranFont: androidx.compose.ui.text.font.FontFamily,
    viewModel: MainViewModel,
    onWordLongClick: (String) -> Unit,
    onAyahLongClick: () -> Unit
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
                    .combinedClickable(
                        enabled = true,
                        onClick = {
                            if (!isRevealed) {
                                // Handled externally via count, but if we want individual reveal:
                            } else {
                                // Default tap
                            }
                        },
                        onLongClick = {
                            if (isRevealed) {
                                onWordLongClick(word)
                            }
                        }
                    )
                    .com.example.ui.swipeWatcher(
                        onSwipeDown = {
                            if (isRevealed) {
                                viewModel.logError(ayah, word, "توقف تام ونسيان الكلمة")
                            }
                        },
                        onSwipeUp = {
                            if (isRevealed) {
                                viewModel.logError(ayah, word, "تردد / شك")
                            }
                        }
                    )
                    .padding(horizontal = 4.dp, vertical = 2.dp)
            )
        }
        
        val ayahErrors = errorLogs.filter { it.surahId == ayah.surahId && it.ayahNumber == ayah.numberInSurah && it.wordText == "[الآية]" }
        val hasAyahError = ayahErrors.isNotEmpty()
        
        val badgeColor = if (hasAyahError) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary
        
        Text(
            text = "﴿${ayah.numberInSurah}﴾",
            fontSize = 32.sp,
            fontFamily = quranFont,
            color = badgeColor.copy(alpha = 0.8f),
            modifier = Modifier
                .combinedClickable(
                    onClick = {},
                    onLongClick = { onAyahLongClick() }
                )
                .padding(horizontal = 8.dp, vertical = 4.dp)
                .align(Alignment.CenterVertically)
        )
    }
}
"""

code = code[:reading_screen_start] + new_reading_screen + "\n" + code[reading_screen_end:]

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)
