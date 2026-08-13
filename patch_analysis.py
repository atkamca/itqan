import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

new_content = """package com.example.ui

import androidx.compose.animation.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
    val diacriticsRegex = "[\\\\u064B-\\\\u065F\\\\u0670]".toRegex()
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
    var searchQuery by remember { mutableStateOf("") }
    val searchResults by viewModel.searchResults.collectAsStateWithLifecycle()
    var activeTab by remember { mutableIntStateOf(0) }
    val isAyahMode = word == "[الآية]"

    ModalBottomSheet(
        onDismissRequest = { 
            viewModel.clearSearch()
            onDismissRequest() 
        },
        windowInsets = WindowInsets(0, 0, 0, 0)
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
                                viewModel.logError(ayah, word, "زيادة حرف", charIndex = index)
                                onDismissRequest()
                            }
                        )
                        
                        if (index < letters.size - 1) {
                            Box(
                                modifier = Modifier
                                    .width(20.dp)
                                    .height(60.dp)
                                    .clickable {
                                        viewModel.logError(ayah, word, "نقصان حرف", charIndex = index)
                                        onDismissRequest()
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Add, contentDescription = "Add", tint = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f), modifier = Modifier.size(16.dp))
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }
}

@Composable
fun InteractiveLetterBox(
    charChunk: String,
    onDiacriticChange: (String) -> Unit,
    onDelete: () -> Unit
) {
    var offsetX by remember { mutableFloatStateOf(0f) }
    var offsetY by remember { mutableFloatStateOf(0f) }
    var showDial by remember { mutableStateOf(false) }
    var isDeleted by remember { mutableStateOf(false) }

    val alpha by animateFloatAsState(targetValue = if (isDeleted) 0.3f else 1f, label = "alpha")

    Box(contentAlignment = Alignment.Center) {
        if (showDial) {
            Box(
                modifier = Modifier
                    .offset(y = (-60).dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(MaterialTheme.colorScheme.primaryContainer)
                    .padding(8.dp)
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("َ", "ُ", "ِ", "ْ").forEach { haraka ->
                        Box(
                            modifier = Modifier
                                .size(32.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.surface)
                                .clickable {
                                    showDial = false
                                    onDiacriticChange(haraka)
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Text(text = "ـ$haraka", fontSize = 20.sp, color = MaterialTheme.colorScheme.onSurface)
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
                            if (offsetX > 100f || offsetX < -100f || offsetY > 100f) {
                                isDeleted = true
                                onDelete()
                            } else if (offsetY < -50f) {
                                showDial = true
                                offsetY = 0f
                                offsetX = 0f
                            } else {
                                offsetX = 0f
                                offsetY = 0f
                                showDial = false
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
"""

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(new_content)
