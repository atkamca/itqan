package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.Ayah
import com.example.ui.theme.Quran_Font

// الدالة المساعدة لفصل الحروف العربية مع حركاتها بشكل صحيح
fun splitArabicLettersWithDiacritics(word: String): List<String> {
    val result = mutableListOf<String>()
    // نطاق الحركات والتشكيل في اليونيكود للغة العربية
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
    var searchQuery by remember { mutableStateOf("") }
    val searchResults by viewModel.searchResults.collectAsStateWithLifecycle()
    var activeTab by remember { mutableIntStateOf(0) }
    val isAyahMode = word == "[الآية]"

    ModalBottomSheet(onDismissRequest = { 
        viewModel.clearSearch()
        onDismissRequest() 
    }) {
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
                // المتشابهات
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
                                Text(text = resultAyah.text, fontFamily = Quran_Font, fontSize = 20.sp, maxLines = 2)
                            }
                        }
                    }
                }
            } else {
                // تفكيك الحروف
                Text("انقر على الحرف لتحديد الخطأ", color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(modifier = Modifier.height(16.dp))
                
                val letters = splitArabicLettersWithDiacritics(word)
                var selectedLetterIndex by remember { mutableStateOf<Int?>(null) }
                
                FlowRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    letters.forEachIndexed { index, charChunk ->
                        val isSelected = selectedLetterIndex == index
                        Box(
                            modifier = Modifier
                                .padding(4.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant)
                                .clickable { selectedLetterIndex = index }
                                .padding(16.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = charChunk, 
                                fontFamily = Quran_Font, 
                                fontSize = 32.sp, 
                                color = if (isSelected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }

                if (selectedLetterIndex != null) {
                    Spacer(modifier = Modifier.height(24.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        Button(
                            onClick = { 
                                viewModel.logError(ayah, word, "خطأ في التشكيل", charIndex = selectedLetterIndex)
                                onDismissRequest() 
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                        ) {
                            Text("✏️ تغيير التشكيل")
                        }
                        Button(
                            onClick = { 
                                viewModel.logError(ayah, word, "زيادة أو نقصان حرف", charIndex = selectedLetterIndex)
                                onDismissRequest() 
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                        ) {
                            Text("✚ إضافة حرف")
                        }
                        Button(
                            onClick = { 
                                viewModel.logError(ayah, word, "زيادة أو نقصان حرف", charIndex = selectedLetterIndex)
                                onDismissRequest() 
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                        ) {
                            Text("✖️ حذف الحرف")
                        }
                    }
                }
            }
        }
    }
}
