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
import androidx.compose.ui.draw.blur
import androidx.compose.ui.input.pointer.PointerEventPass
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
    val snackbarHostState = remember { SnackbarHostState() }
    val snackbarMessage by viewModel.snackbarMessage.collectAsStateWithLifecycle()

    LaunchedEffect(snackbarMessage) {
        snackbarMessage?.let { msg ->
            val result = snackbarHostState.showSnackbar(
                message = msg,
                actionLabel = "تراجع",
                duration = SnackbarDuration.Short
            )
            if (result == SnackbarResult.ActionPerformed) {
                viewModel.undoLastError()
            }
            viewModel.clearSnackbar()
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        bottomBar = {
            androidx.compose.material3.Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .navigationBarsPadding()
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
    

    
    LaunchedEffect(jumpIndex) {
        if (jumpIndex != -1 && jumpIndex < currentAyahs.size) {
            pagerState.scrollToPage(jumpIndex)
            viewModel.resetJumpIndex()
        }
    }

    LaunchedEffect(pagerState.currentPage, isRevisionMode) {
        revealedWordsCount = 0

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
        containerColor = MaterialTheme.colorScheme.background
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
                val totalAyahs = com.example.data.QuranData.surahs.find { it.id == selectedSurahId }?.ayahCount ?: 1
                AyahJumpDialog(
                    currentAyah = currentAyah?.numberInSurah ?: 1,
                    totalAyahs = totalAyahs,
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

            val annotatedWord = buildAnnotatedString {
                val errorChars = wordErrors.mapNotNull { it.charIndex }
                word.forEachIndexed { i, c ->
                    if (i in errorChars) {
                        withStyle(SpanStyle(color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Black, textDecoration = TextDecoration.Underline)) { append(c.toString()) }
                    } else {
                        append(c.toString())
                    }
                }
            }
            
            val blurRadius = if (!isRevealed) 12.dp else 0.dp

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
                                    if (!isRevealed) {
                                        onRevealWord(index + 1)
                                    }
                                },
                                onLongPress = {
                                    if (isRevealed) {
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
                    onWordLongClick("[الآية]")
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
    val errorLogs by viewModel.errorLogs.collectAsStateWithLifecycle()
    var showClearDialog by remember { mutableStateOf(false) }

    if (showClearDialog) {
        AlertDialog(
            onDismissRequest = { showClearDialog = false },
            title = { Text("مسح السجل") },
            text = { Text("هل أنت متأكد من مسح جميع الأخطاء المسجلة؟ لا يمكن التراجع عن هذا الإجراء.") },
            confirmButton = {
                TextButton(onClick = { 
                    viewModel.clearLogs()
                    showClearDialog = false 
                }) {
                    Text("مسح", color = MaterialTheme.colorScheme.error)
                }
            },
            dismissButton = {
                TextButton(onClick = { showClearDialog = false }) {
                    Text("إلغاء")
                }
            }
        )
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("تقرير الأخطاء", fontWeight = FontWeight.Bold) },
                actions = {
                    if (errorLogs.isNotEmpty()) {
                        IconButton(onClick = { showClearDialog = true }) {
                            Icon(Icons.Default.Delete, contentDescription = "مسح السجل", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }
            )
        },
        containerColor = MaterialTheme.colorScheme.background
    ) { paddingValues ->
        if (errorLogs.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize().padding(paddingValues), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.Analytics, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.surfaceVariant)
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("لا توجد أخطاء مسجلة بعد. أحسنت!", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 18.sp)
                }
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(paddingValues),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(errorLogs) { log ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "${log.surahName} - آية ${log.ayahNumber}",
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.primary,
                                    fontSize = 16.sp
                                )
                                val dateFormat = android.text.format.DateFormat.format("yyyy-MM-dd HH:mm", log.timestamp)
                                Text(text = dateFormat.toString(), fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Text(
                                text = "الكلمة: ${log.wordText}",
                                fontFamily = com.example.ui.theme.Quran_Font,
                                fontSize = 24.sp
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.FlashOn, contentDescription = null, tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(text = log.errorType, color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Bold)
                            }
                            
                            if (!log.readText.isNullOrEmpty()) {
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(text = "تمت قراءتها: ${log.readText}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                            }
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SurahDropdown(selectedSurahId: Int, onSurahSelected: (Int) -> Unit) {
    var showSheet by remember { mutableStateOf(false) }
    val surahs = com.example.data.QuranData.surahs
    val selectedSurah = surahs.find { it.id == selectedSurahId }
    
    TextButton(onClick = { showSheet = true }, modifier = Modifier.clip(RoundedCornerShape(8.dp))) {
        Text(
            text = selectedSurah?.name ?: "السورة",
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
    }

    if (showSheet) {
        ModalBottomSheet(onDismissRequest = { showSheet = false }) {
            Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)) {
                Text("اختر السورة", fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))
                LazyColumn(modifier = Modifier.fillMaxWidth()) {
                    items(surahs) { surah ->
                        val isSelected = surah.id == selectedSurahId
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .background(if (isSelected) MaterialTheme.colorScheme.primaryContainer else Color.Transparent)
                                .clickable {
                                    onSurahSelected(surah.id)
                                    showSheet = false
                                }
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(surah.name, fontSize = 18.sp, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal, color = if(isSelected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface)
                            Text("${surah.ayahCount} آية", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun AyahJumpDialog(currentAyah: Int, totalAyahs: Int, onDismiss: () -> Unit, onJump: (Int) -> Unit) {
    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)) {
            Text("الانتقال إلى آية", fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))
            
            LazyColumn(modifier = Modifier.fillMaxWidth().weight(1f, fill = false)) {
                item {
                    FlowRow(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        for (i in 1..totalAyahs) {
                            val isSelected = i == currentAyah
                            Box(
                                modifier = Modifier
                                    .size(60.dp)
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)
                                    .clickable { onJump(i) },
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = i.toString(),
                                    fontSize = 18.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}
