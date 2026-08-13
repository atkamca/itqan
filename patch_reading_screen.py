import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

old_pager = """HorizontalPager(
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
                            onRevealWord = { newCount -> revealedWordsCount = newCount },
                            errorLogs = errorLogs,
                            quranFont = quranFont,
                            viewModel = viewModel,
                            onWordLongClick = { w -> selectedWordForAnalysis = Pair(ayah, w) }
                        )
                        
                    }
                }
            }"""

new_pager = """HorizontalPager(
                state = pagerState,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth(),
            ) { page ->
                val ayah = currentAyahs[page]
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(horizontal = 24.dp, vertical = 24.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .wrapContentHeight()
                            .padding(bottom = 80.dp),
                        shape = androidx.compose.foundation.shape.RoundedCornerShape(24.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .verticalScroll(rememberScrollState())
                                .padding(horizontal = 24.dp, vertical = 40.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            // Page/Ayah decoration (e.g. Bismillah if Ayah 1)
                            if (ayah.numberInSurah == 1 && ayah.surahId != 1 && ayah.surahId != 9) {
                                Text("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", fontFamily = quranFont, fontSize = 28.sp, color = MaterialTheme.colorScheme.primary, textAlign = TextAlign.Center)
                                Spacer(modifier = Modifier.height(24.dp))
                            }
                            
                            AyahDisplayView(
                                ayah = ayah,
                                isRevisionMode = isRevisionMode,
                                revealedWordsCount = revealedWordsCount,
                                onRevealWord = { newCount -> revealedWordsCount = newCount },
                                errorLogs = errorLogs,
                                quranFont = quranFont,
                                viewModel = viewModel,
                                onWordLongClick = { w -> selectedWordForAnalysis = Pair(ayah, w) }
                            )
                            
                            Spacer(modifier = Modifier.height(32.dp))
                            
                            // End of Ayah marker
                            Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.5f), CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = "﴿${ayah.numberInSurah}﴾", 
                                    fontFamily = com.example.ui.theme.UI_Font, 
                                    fontSize = 18.sp, 
                                    color = MaterialTheme.colorScheme.primary,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                }
            }"""

code = code.replace(old_pager, new_pager)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)

print("Updated Reading Screen Cards")
