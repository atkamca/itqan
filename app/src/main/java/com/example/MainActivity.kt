package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.clickable
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.Analytics
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.FlashOn
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material3.*
import androidx.compose.runtime.*

import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateOf

import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.data.Ayah
import com.example.data.ErrorLogEntity
import com.example.data.QuranData
import com.example.ui.MainViewModel
import com.example.ui.theme.MyApplicationTheme
import kotlinx.coroutines.launch
import kotlin.math.max

val wordErrorTypes = listOf(
    "تردد / توقف سريع", 
    "خطأ في التشكيل", 
    "زيادة أو نقصان حرف", 
    "تغيير كلمة بكلمة أخرى (متشابهات)",
    "إضافة كلمة زائدة", 
    "نسيان كلمة وتجاوزها", 
    "توقف تام ونسيان الكلمة",
    "تردد مع تصحيح ذاتي", 
    "توقف وتفكير لعدة ثوانٍ"
)

val ayahErrorTypes = listOf(
    "نسيان بداية الآية", "خطأ في الربط بين الآيات / قفز لآية أخرى", "نسيان نهاية الآية"
)

fun getCategoryForError(type: String): String {
    return when (type) {
        "خطأ في التشكيل" -> "أخطاء التشكيل"
        "زيادة أو نقصان حرف", "إضافة كلمة زائدة", "نسيان كلمة وتجاوزها", "توقف تام ونسيان الكلمة" -> "أخطاء الحفظ والتغيير"
        "تغيير كلمة بكلمة أخرى (متشابهات)", "نسيان بداية الآية", "خطأ في الربط بين الآيات / قفز لآية أخرى", "نسيان نهاية الآية" -> "أخطاء الربط والمتشابهات"
        "تردد مع تصحيح ذاتي", "توقف وتفكير لعدة ثوانٍ", "تردد في الآية الحالية", "توقف واستعانة بالتذكير", "تردد / توقف سريع" -> "حالات التردد"
        else -> "أخرى"
    }
}

fun getErrorWeight(type: String): Int {
    return when (type) {
        "تردد / توقف سريع", "تردد مع تصحيح ذاتي", "تردد في الآية الحالية", "توقف وتفكير لعدة ثوانٍ", "توقف واستعانة بالتذكير" -> 1
        "خطأ في التشكيل" -> 2
        "زيادة أو نقصان حرف", "إضافة كلمة زائدة", "نسيان كلمة وتجاوزها" -> 3
        "تغيير كلمة بكلمة أخرى (متشابهات)" -> 4
        "توقف تام ونسيان الكلمة", "نسيان بداية الآية", "نسيان نهاية الآية" -> 5
        "خطأ في الربط بين الآيات / قفز لآية أخرى" -> 6
        else -> 3
    }
}

fun getErrorColor(type: String, defaultColor: Color): Color {
    return when (type) {
        "خطأ في التشكيل" -> Color(0xFFE65100) // Orange
        "تردد / توقف سريع", "تردد مع تصحيح ذاتي", "تردد في الآية الحالية", "توقف وتفكير لعدة ثوانٍ", "توقف واستعانة بالتذكير" -> Color(0xFFF57F17) // Gold/Yellow
        "زيادة أو نقصان حرف", "تغيير كلمة بكلمة أخرى (متشابهات)", "إضافة كلمة زائدة", "نسيان كلمة وتجاوزها", "توقف تام ونسيان الكلمة" -> Color(0xFFD32F2F) // Red
        else -> defaultColor
    }
}

class MainActivity : ComponentActivity() {
    private var crashMessage by mutableStateOf<String?>(null)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
                MyApplicationTheme {
                    val viewModel: MainViewModel = viewModel()
                    MorakebApp(viewModel)
                }
            }
        }
    }
}

@Composable
fun MorakebApp(viewModel: MainViewModel) {
    var selectedTab by remember { mutableIntStateOf(0) }
    Scaffold(
        bottomBar = {
            androidx.compose.material3.Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(24.dp),
                shadowElevation = 8.dp,
                color = MaterialTheme.colorScheme.surface
            ) {
                NavigationBar(
                    containerColor = androidx.compose.ui.graphics.Color.Transparent,
                    tonalElevation = 0.dp,
                    windowInsets = WindowInsets(0, 0, 0, 0)
                ) {
                    NavigationBarItem(
                        icon = { Icon(Icons.Filled.MenuBook, contentDescription = "المراجعة") },
                        label = { Text("المراجعة", fontWeight = FontWeight.Bold) },
                        selected = selectedTab == 0,
                        onClick = { selectedTab = 0 },
                        colors = NavigationBarItemDefaults.colors(
                            indicatorColor = MaterialTheme.colorScheme.primaryContainer,
                            selectedIconColor = MaterialTheme.colorScheme.onPrimaryContainer,
                            selectedTextColor = MaterialTheme.colorScheme.primary
                        )
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Filled.Analytics, contentDescription = "التقارير") },
                        label = { Text("التقارير", fontWeight = FontWeight.Bold) },
                        selected = selectedTab == 1,
                        onClick = { selectedTab = 1 },
                        colors = NavigationBarItemDefaults.colors(
                            indicatorColor = MaterialTheme.colorScheme.primaryContainer,
                            selectedIconColor = MaterialTheme.colorScheme.onPrimaryContainer,
                            selectedTextColor = MaterialTheme.colorScheme.primary
                        )
                    )
                }
            }
        },
        containerColor = MaterialTheme.colorScheme.background
    ) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding)) {
            if (selectedTab == 0) {
                ReadingScreen(viewModel)
            } else {
                ReportsScreen(viewModel)
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class, ExperimentalLayoutApi::class)
@Composable
fun ReadingScreen(viewModel: MainViewModel) {
    val currentAyahs by viewModel.currentAyahs.collectAsStateWithLifecycle()
    val errorLogs by viewModel.errorLogs.collectAsStateWithLifecycle()
    val selectedSurahId by viewModel.selectedSurahId.collectAsStateWithLifecycle()
    val jumpIndex by viewModel.jumpToAyahIndex.collectAsStateWithLifecycle()
    
    val pagerState = rememberPagerState(pageCount = { currentAyahs.size })
    val coroutineScope = rememberCoroutineScope()
    
    // true = Active Reading Mode (words hidden, quick actions)
    // false = Analysis Mode (words shown, bottom sheet on long press)
    var isRevisionMode by remember { mutableStateOf(true) }
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
            if (isRevisionMode && nextAyah != null) {
                ExtendedFloatingActionButton(
                    onClick = { /* Handled by combinedClickable below */ },
                    icon = { Icon(Icons.Default.Visibility, contentDescription = null) },
                    text = { Text("الآية الموالية") },
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
                    modifier = Modifier.combinedClickable(
                        onClick = {
                            if (!isNextAyahVisible) {
                                isNextAyahVisible = true
                                revealedNextWordCount = 0
                            } else {
                                val nextAyahWords = nextAyah.text.split("\\s+".toRegex()).filter { it.isNotBlank() }
                                if (revealedNextWordCount < nextAyahWords.size) {
                                    revealedNextWordCount++
                                } else {
                                    coroutineScope.launch {
                                        pagerState.animateScrollToPage(pagerState.currentPage + 1)
                                    }
                                }
                            }
                        },
                        onLongClick = {
                            // Long press to reveal entire next ayah
                            isNextAyahVisible = true
                            revealedNextWordCount = nextAyah.text.split("\\s+".toRegex()).filter { it.isNotBlank() }.size
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
                        Text(if (isRevisionMode) "تلاوة" else "تحليل", modifier = Modifier.padding(end = 8.dp))
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
                            onRevealWord = { newCount -> revealedWordsCount = newCount },
                            errorLogs = errorLogs,
                            quranFont = quranFont,
                            viewModel = viewModel,
                            onWordLongClick = { w -> selectedWordForAnalysis = Pair(ayah, w) }
                        )
                        
                        if (page == pagerState.currentPage && isNextAyahVisible && nextAyah != null) {
                            Spacer(modifier = Modifier.height(32.dp))
                            Divider(modifier = Modifier.padding(horizontal = 32.dp))
                            Spacer(modifier = Modifier.height(32.dp))
                            AyahDisplayView(
                                ayah = nextAyah,
                                isRevisionMode = isRevisionMode,
                                revealedWordsCount = revealedNextWordCount,
                                onRevealWord = { newCount -> revealedNextWordCount = newCount },
                                errorLogs = errorLogs,
                                quranFont = quranFont,
                                viewModel = viewModel,
                                onWordLongClick = { w -> selectedWordForAnalysis = Pair(nextAyah, w) }
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
    onRevealWord: (Int) -> Unit,
    errorLogs: List<ErrorLogEntity>,
    quranFont: androidx.compose.ui.text.font.FontFamily,
    viewModel: MainViewModel,
    onWordLongClick: (String) -> Unit
) {
    val words = ayah.text.split("\\s+".toRegex()).filter { it.isNotBlank() }
    
    // Track which word has the popup open
    var activePopupWordIndex by remember { mutableStateOf<Int?>(null) }
    
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
                        .combinedClickable(
                            enabled = true,
                            onClick = {
                                if (isRevisionMode) {
                                    if (!isRevealed) {
                                        // Reveal word and log hesitate
                                        onRevealWord(index + 1)
                                        viewModel.logError(ayah, word, "تردد / تعثر")
                                    } else {
                                        // Word is already revealed in reading mode -> show quick actions popup
                                        activePopupWordIndex = if (activePopupWordIndex == index) null else index
                                    }
                                } else {
                                    // In analysis mode, tapping does nothing specific unless we want
                                    activePopupWordIndex = null
                                }
                            },
                            onLongClick = {
                                if (!isRevisionMode && isRevealed) {
                                    // Analysis Mode -> Long press shows Bottom Sheet
                                    onWordLongClick(word)
                                }
                            }
                        )
                        .padding(horizontal = 4.dp, vertical = 2.dp)
                )
                
                // Quick Action Popup (only in Revision Mode for revealed words)
                if (isRevisionMode && activePopupWordIndex == index) {
                    DropdownMenu(
                        expanded = true,
                        onDismissRequest = { activePopupWordIndex = null },
                        modifier = Modifier.background(MaterialTheme.colorScheme.surface)
                    ) {
                        DropdownMenuItem(
                            text = { Text("🔴 خطأ", fontWeight = FontWeight.Bold) },
                            onClick = {
                                viewModel.logError(ayah, word, "توقف تام ونسيان الكلمة")
                                activePopupWordIndex = null
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("🟡 تردد", fontWeight = FontWeight.Bold) },
                            onClick = {
                                viewModel.logError(ayah, word, "تردد / شك")
                                activePopupWordIndex = null
                            }
                        )
                    }
                }
            }
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
                .padding(horizontal = 8.dp, vertical = 4.dp)
                .align(Alignment.CenterVertically)
        )
    }
}


@Composable
fun SurahDropdown(selectedSurahId: Int, onSurahSelected: (Int) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    val surahs = com.example.data.QuranData.surahs
    val selectedSurah = surahs.find { it.id == selectedSurahId }
    
    Box {
        TextButton(onClick = { expanded = true }) {
            Text(
                text = selectedSurah?.name ?: "السورة",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )
        }
        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false },
            modifier = Modifier.heightIn(max = 300.dp)
        ) {
            surahs.forEach { surah ->
                DropdownMenuItem(
                    text = { Text(surah.name) },
                    onClick = {
                        onSurahSelected(surah.id)
                        expanded = false
                    }
                )
            }
        }
    }
}

@Composable
fun AyahJumpDialog(currentAyah: Int, onDismiss: () -> Unit, onJump: (Int) -> Unit) {
    var text by remember { mutableStateOf(currentAyah.toString()) }
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("الانتقال لآية") },
        text = {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it.filter { char -> char.isDigit() } },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
        },
        confirmButton = {
            TextButton(onClick = {
                text.toIntOrNull()?.let { onJump(it) }
            }) {
                Text("انتقال")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("إلغاء")
            }
        }
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReportsScreen(viewModel: MainViewModel) {
    val errorLogs by viewModel.errorLogs.collectAsStateWithLifecycle()
    
    // Dynamic Mastery Index & Recovery Tracking Logic (Last 30 Days)
    val thirtyDaysAgo = System.currentTimeMillis() - (30L * 24 * 60 * 60 * 1000)
    val recentErrors = errorLogs.filter { it.timestamp >= thirtyDaysAgo }
    
    val todayStart = System.currentTimeMillis() - (24 * 60 * 60 * 1000)
    val groupedErrors = recentErrors.groupBy { "${it.surahId}-${it.ayahNumber}-${it.wordText}" }
    
    val fixedErrors = mutableListOf<ErrorLogEntity>()
    val chronicErrors = mutableListOf<Pair<ErrorLogEntity, Int>>()
    
    var recoveryBonus = 0
    groupedErrors.forEach { (_, logs) ->
        val sortedLogs = logs.sortedBy { it.timestamp }
        val latestLog = sortedLogs.last()
        val hasErrorTodayInSurah = recentErrors.any { it.surahId == latestLog.surahId && it.timestamp >= todayStart }
        
        if (latestLog.timestamp < todayStart && hasErrorTodayInSurah) {
            fixedErrors.add(latestLog)
            recoveryBonus += 5 // +5 points for every fixed error
        } else if (sortedLogs.size >= 2) {
            chronicErrors.add(Pair(latestLog, sortedLogs.size))
        }
    }
    
    val totalPenalty = recentErrors.sumOf { getErrorWeight(it.errorType) }
    val rawGMI = 100 - totalPenalty + recoveryBonus
    val finalGMI = rawGMI.coerceIn(0, 100)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        TopAppBar(
            title = { Text("التقارير ونقاط الضعف", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleLarge) },
            actions = {
                if (errorLogs.isNotEmpty()) {
                    IconButton(onClick = { viewModel.clearLogs() }) {
                        Icon(Icons.Filled.Delete, contentDescription = "مسح السجل", tint = MaterialTheme.colorScheme.error)
                    }
                }
            },
            colors = TopAppBarDefaults.topAppBarColors(
                containerColor = MaterialTheme.colorScheme.surfaceVariant,
                titleContentColor = MaterialTheme.colorScheme.onSurfaceVariant
            )
        )

        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 16.dp),
            contentPadding = PaddingValues(vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            item {
                ElevatedCard(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(24.dp),
                    elevation = CardDefaults.elevatedCardElevation(defaultElevation = 0.dp),
                    colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
                ) {
                    Column(
                        modifier = Modifier.padding(32.dp).fillMaxWidth(),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text("مؤشر الإتقان (GMI)", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f))
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("٪$finalGMI", style = MaterialTheme.typography.displayLarge, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onPrimaryContainer)
                        
                        Spacer(modifier = Modifier.height(32.dp))
                        
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceEvenly
                        ) {
                            StatItem("معامل التعافي", "+$recoveryBonus")
                            StatItem("إجمالي الأخطاء", "${recentErrors.size}")
                        }
                        
                        Spacer(modifier = Modifier.height(32.dp))
                        
                        Text(
                            text = "يتم الحساب بناءً على أداء آخر 30 يوماً",
                            style = MaterialTheme.typography.labelMedium,
                            textAlign = TextAlign.Center,
                            color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.6f)
                        )
                    }
                }
            }

            if (fixedErrors.isNotEmpty()) {
                item {
                    Text("✅ تم إصلاحها بنجاح هذا الأسبوع", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                }
                items(fixedErrors.take(5)) { log ->
                    ElevatedCard(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)),
                        elevation = CardDefaults.elevatedCardElevation(defaultElevation = 1.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(20.dp).fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text(log.wordText, fontSize = 22.sp, fontFamily = FontFamily.Serif, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("${log.surahName} - آية ${log.ayahNumber}", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.8f))
                            }
                            Badge(containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.onPrimary) { 
                                Text("مُعالج", modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }

            if (chronicErrors.isNotEmpty()) {
                item {
                    Text("⚠️ أشد المواضع حرجاً (أخطاء متكررة)", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.error)
                }
                items(chronicErrors.sortedByDescending { it.second }.take(5)) { (log, count) ->
                    ElevatedCard(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.elevatedCardColors(containerColor = MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.8f)),
                        elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(20.dp).fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text(log.wordText, fontSize = 22.sp, fontFamily = FontFamily.Serif, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onErrorContainer)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("${log.surahName} - آية ${log.ayahNumber}", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onErrorContainer.copy(alpha = 0.8f))
                                Spacer(modifier = Modifier.height(2.dp))
                                Text("الخطأ: ${log.errorType}", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onErrorContainer)
                            }
                            Badge(containerColor = MaterialTheme.colorScheme.error, contentColor = MaterialTheme.colorScheme.onError) { 
                                Text("تكرر $count مرات", modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }

            if (recentErrors.isNotEmpty()) {
                val comparisonErrors = recentErrors.filter { !it.readText.isNullOrBlank() }
                if (comparisonErrors.isNotEmpty()) {
                    item {
                        Text("مقارنة القراءات الخاطئة", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                    }
                    items(comparisonErrors) { log ->
                        Card(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Row(
                                modifier = Modifier.padding(16.dp).fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                val annotatedOriginal = buildAnnotatedString {
                                    log.wordText.forEachIndexed { i, c ->
                                        if (i == log.charIndex) {
                                            withStyle(SpanStyle(color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Black, textDecoration = TextDecoration.Underline)) { append(c.toString()) }
                                        } else {
                                            append(c.toString())
                                        }
                                    }
                                }
                                Text(text = annotatedOriginal, fontSize = 22.sp, fontFamily = FontFamily.Serif, fontWeight = FontWeight.Bold)
                                
                                Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, tint = MaterialTheme.colorScheme.outline)
                                
                                Text(text = log.readText!!, fontSize = 22.sp, fontFamily = FontFamily.Serif, color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Bold)
                            }
                            Text("الخطأ: ${log.errorType}", modifier = Modifier.padding(start = 16.dp, bottom = 12.dp), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
                
                item {
                    Text("تحليل نقاط الضعف", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                }
                
                val categorized = recentErrors.groupBy { getCategoryForError(it.errorType) }
                items(categorized.entries.toList().sortedByDescending { it.value.size }) { (category, logs) ->
                    val percentage = (logs.size.toFloat() / recentErrors.size)
                    Column(modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text(category, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold)
                            Text("${(percentage * 100).toInt()}٪ (${logs.size})", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.secondary)
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        LinearProgressIndicator(
                            progress = { percentage },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(12.dp)
                                .clip(RoundedCornerShape(6.dp)),
                            color = MaterialTheme.colorScheme.primary,
                            trackColor = MaterialTheme.colorScheme.primaryContainer
                        )
                    }
                }

                item {
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("أكثر الكلمات التي بها أخطاء", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                }
                val weakPoints = recentErrors.filter { it.wordText != "[الآية]" }.groupBy { it.wordText }.map { it.key to it.value.size }.sortedByDescending { it.second }
                items(weakPoints.take(10)) { (word, count) ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(word, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Serif, fontSize = 20.sp)
                        Badge { Text("$count", modifier = Modifier.padding(4.dp), fontSize = 14.sp) }
                    }
                    HorizontalDivider(thickness = 0.5.dp, color = MaterialTheme.colorScheme.outlineVariant)
                }
            } else {
                item {
                    Box(modifier = Modifier
                        .fillMaxWidth()
                        .padding(32.dp), contentAlignment = Alignment.Center) {
                        Text("لا توجد أخطاء مسجلة في آخر 30 يوماً.\nاستمر في القراءة والمراجعة!", textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant, lineHeight = 24.sp)
                    }
                }
            }
        }
    }
}

@Composable
fun StatItem(label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(value, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.height(4.dp))
        Text(label, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
