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

import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.material3.minimumInteractiveComponentSize

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

@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun ReportsScreen(viewModel: MainViewModel) {
    // Just a placeholder so it compiles
    androidx.compose.foundation.layout.Box(androidx.compose.ui.Modifier.fillMaxSize())
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
                fontWeight = androidx.compose.ui.text.font.FontWeight.Bold
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
                keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number)
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
