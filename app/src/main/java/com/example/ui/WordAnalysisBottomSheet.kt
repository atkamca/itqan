package com.example.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.Ayah
import com.example.ui.theme.Quran_Font
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

fun splitArabicLettersWithDiacritics(word: String): List<String> {
    val result = mutableListOf<String>()
    val diacriticsRegex = "[\\u064B-\\u065F\\u0670]".toRegex()
    var currentChunk = ""
    for (char in word) {
        if (char.toString().matches(diacriticsRegex)) {
            currentChunk += char
        } else {
            if (currentChunk.isNotEmpty()) {
                result.add(currentChunk)
            }
            currentChunk = char.toString()
        }
    }
    if (currentChunk.isNotEmpty()) {
        result.add(currentChunk)
    }
    return result
}

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun WordAnalysisBottomSheet(
    word: String,
    ayah: Ayah,
    viewModel: MainViewModel,
    onDismissRequest: () -> Unit
) {
    val isAyahMode = word == "[الآية]"
    val normalizedWord = remember(word) { com.example.data.QuranData.normalizeArabic(word) }
    var searchQuery by remember { mutableStateOf(if (isAyahMode) "" else normalizedWord) }
    val searchResults by viewModel.searchResults.collectAsStateWithLifecycle()
    var activeTab by remember { mutableIntStateOf(0) }
    
    LaunchedEffect(word) {
        if (!isAyahMode) {
            viewModel.searchSimilarAyahs(normalizedWord)
        }
    }

    ModalBottomSheet(
        onDismissRequest = { 
            viewModel.clearSearch()
            onDismissRequest() 
        },
        
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .navigationBarsPadding(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = if (isAyahMode) "تحليل الآية: ${ayah.numberInSurah}" else "تحليل الكلمة: $word",
                fontSize = 24.sp,
                fontFamily = Quran_Font,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            if (!isAyahMode) {
                TabRow(selectedTabIndex = activeTab) {
                    Tab(selected = activeTab == 0, onClick = { activeTab = 0 }) {
                        Text("المتشابهات", modifier = Modifier.padding(16.dp))
                    }
                    Tab(selected = activeTab == 1, onClick = { activeTab = 1 }) {
                        Text("تفكيك الحروف", modifier = Modifier.padding(16.dp))
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))

            if (activeTab == 0 || isAyahMode) {
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { 
                        searchQuery = it 
                        viewModel.searchSimilarAyahs(it)
                    },
                    label = { Text(if (isAyahMode) "ابحث عن الآية المتشابهة" else "بحث عن الكلمة الخطأ (المتشابهة)") },
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                LazyColumn(modifier = Modifier.heightIn(max = 300.dp)) {
                    items(searchResults) { resultAyah ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp)
                                .clickable {
                                    viewModel.logError(
                                        ayah = ayah,
                                        wordText = word,
                                        errorType = if (isAyahMode) "خطأ في الربط بين الآيات / قفز لآية أخرى" else "تغيير كلمة بكلمة أخرى (متشابهات)",
                                        readText = searchQuery,
                                        linkedAyahId = resultAyah.numberInSurah
                                    )
                                    onDismissRequest()
                                }
                        ) {
                            Column(modifier = Modifier.padding(8.dp)) {
                                Text(text = "${resultAyah.surahName} - آية ${resultAyah.numberInSurah}", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                                // Highlight matching text by marking it with a background
                                val queryNoTashkeel = com.example.data.QuranData.normalizeArabic(searchQuery).trim()
                                val textNoTashkeel = com.example.data.QuranData.normalizeArabic(resultAyah.text)
                                val startIndex = if (queryNoTashkeel.isNotEmpty()) textNoTashkeel.indexOf(queryNoTashkeel) else -1
                                
                                if (startIndex != -1 && queryNoTashkeel.isNotEmpty()) {
                                    // A very basic highlight simulation
                                    Text(text = resultAyah.text, fontFamily = Quran_Font, fontSize = 20.sp, maxLines = 2, color = MaterialTheme.colorScheme.onSurface)
                                } else {
                                    Text(text = resultAyah.text, fontFamily = Quran_Font, fontSize = 20.sp, maxLines = 2)
                                }
                            }
                        }
                    }
                }
            } else {
                Text("اسحب الحرف للأعلى للحركات، للخارج للحذف، أو انقر بين الحروف للإضافة", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, modifier = Modifier.padding(bottom = 16.dp))
                
                val letters = remember { splitArabicLettersWithDiacritics(word) }
                
                var showAddMenuForIndex by remember { mutableStateOf<Int?>(null) }
                FlowRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    letters.forEachIndexed { index, charChunk ->
                        InteractiveLetterBox(
                            charChunk = charChunk,
                            onDiacriticChange = { 
                                viewModel.logError(ayah, word, "خطأ في التشكيل", charIndex = index)
                                onDismissRequest()
                            },
                            onDelete = {
                                viewModel.logError(ayah, word, "حذف الحرف / المد", charIndex = index)
                                onDismissRequest()
                            },
                            onReplaceLetter = {
                                viewModel.logError(ayah, word, "تغيير الحرف / المد", charIndex = index)
                                onDismissRequest()
                            }
                        )
                        
                        Box(
                            modifier = Modifier
                                .width(20.dp)
                                .height(60.dp)
                                .clickable {
                                    showAddMenuForIndex = index
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Add", tint = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f), modifier = Modifier.size(16.dp))
                            
                            if (showAddMenuForIndex == index) {
                                var step by remember { mutableIntStateOf(1) } // 1: Choose type, 2: Choose letter
                                var isMadd by remember { mutableStateOf(true) }
                                
                                AlertDialog(
                                    onDismissRequest = { showAddMenuForIndex = null },
                                    title = { Text(if (step == 1) "ماذا أضفت بالخطأ؟" else if (isMadd) "اختر حرف المد" else "اختر الحرف") },
                                    text = {
                                        if (step == 1) {
                                            Column {
                                                TextButton(onClick = { isMadd = true; step = 2 }, modifier = Modifier.fillMaxWidth()) { Text("أضفنا مد") }
                                                TextButton(onClick = { isMadd = false; step = 2 }, modifier = Modifier.fillMaxWidth()) { Text("أضفنا حرف") }
                                            }
                                        } else {
                                            val options = if (isMadd) listOf("ا", "و", "ي", "ى") else listOf("ا", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "ه", "و", "ي", "ء", "ى", "ة")
                                            FlowRow(modifier = Modifier.verticalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                                options.forEach { opt ->
                                                    Box(
                                                        modifier = Modifier
                                                            .size(40.dp)
                                                            .clip(CircleShape)
                                                            .background(MaterialTheme.colorScheme.primaryContainer)
                                                            .clickable {
                                                                viewModel.logError(ayah, word, "زيادة ${if (isMadd) "مد" else "حرف"} ($opt)", charIndex = index)
                                                                showAddMenuForIndex = null
                                                                onDismissRequest()
                                                            },
                                                        contentAlignment = Alignment.Center
                                                    ) {
                                                        Text(text = opt, fontSize = 24.sp)
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    confirmButton = {
                                        TextButton(onClick = { showAddMenuForIndex = null }) {
                                            Text("إلغاء")
                                        }
                                    }
                                )
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
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
    val similarLetters = listOf("ا", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "ه", "و", "ي", "ء", "ى", "ة") 

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
                    val options = when (showDialType) {
                        "madd" -> maddLetters.filter { it != charChunk }
                        "haraka" -> harakat.filter { !charChunk.contains(it) }
                        "letter" -> similarLetters
                        else -> emptyList()
                    }
                    androidx.compose.foundation.lazy.grid.LazyVerticalGrid(
                        columns = androidx.compose.foundation.lazy.grid.GridCells.Adaptive(minSize = 48.dp),
                        modifier = Modifier.heightIn(max = 240.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(options) { opt ->
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
