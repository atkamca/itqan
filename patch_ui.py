import re

code = """package com.example.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.Ayah
import com.example.data.normalizeQuranText
import com.example.ui.theme.Quran_Font
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

fun splitIntoGraphemes(word: String): List<String> {
    val iterator = java.text.BreakIterator.getCharacterInstance()
    iterator.setText(word)
    val graphemes = mutableListOf<String>()
    var start = iterator.first()
    var end = iterator.next()
    while (end != java.text.BreakIterator.DONE) {
        graphemes.add(word.substring(start, end))
        start = end
        end = iterator.next()
    }
    return graphemes
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
    val normalizedWord = remember(word) { word.normalizeQuranText() }
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
                                val queryNoTashkeel = searchQuery.normalizeQuranText().trim()
                                val textNoTashkeel = resultAyah.text.normalizeQuranText()
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
                Text(
                    "انقر على الحرف لتحديد الخطأ", 
                    color = MaterialTheme.colorScheme.onSurfaceVariant, 
                    fontSize = 14.sp, 
                    modifier = Modifier.padding(bottom = 16.dp)
                )
                
                val letters = remember { splitIntoGraphemes(word) }
                var selectedLetterIndex by remember { mutableStateOf<Int?>(null) }
                
                CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
                    FlowRow(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Center,
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        letters.forEachIndexed { index, charChunk ->
                            val isSelected = selectedLetterIndex == index
                            Box(
                                modifier = Modifier
                                    .padding(horizontal = 4.dp)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.secondaryContainer)
                                    .clickable {
                                        selectedLetterIndex = if (isSelected) null else index
                                    }
                                    .padding(16.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = charChunk,
                                    fontFamily = Quran_Font,
                                    fontSize = 36.sp,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSecondaryContainer
                                )
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                if (selectedLetterIndex != null) {
                    Column(
                        modifier = Modifier.fillMaxWidth(),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Button(
                            onClick = {
                                viewModel.logError(ayah, word, "تغيير التشكيل أو العلامة", charIndex = selectedLetterIndex)
                                onDismissRequest()
                            },
                            modifier = Modifier.fillMaxWidth(),
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                        ) {
                            Icon(Icons.Default.Edit, contentDescription = null, modifier = Modifier.size(18.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("تغيير التشكيل أو العلامة", fontSize = 16.sp)
                        }
                        
                        Button(
                            onClick = {
                                viewModel.logError(ayah, word, "إضافة حرف زائد", charIndex = selectedLetterIndex)
                                onDismissRequest()
                            },
                            modifier = Modifier.fillMaxWidth(),
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.tertiary)
                        ) {
                            Icon(Icons.Default.Add, contentDescription = null, modifier = Modifier.size(18.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("إضافة حرف زائد", fontSize = 16.sp)
                        }
                        
                        Button(
                            onClick = {
                                viewModel.logError(ayah, word, "حذف الحرف", charIndex = selectedLetterIndex)
                                onDismissRequest()
                            },
                            modifier = Modifier.fillMaxWidth(),
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                        ) {
                            Icon(Icons.Default.Close, contentDescription = null, modifier = Modifier.size(18.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("حذف الحرف", fontSize = 16.sp)
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }
}
"""

with open('app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)

print("Updated WordAnalysisBottomSheet.kt")
