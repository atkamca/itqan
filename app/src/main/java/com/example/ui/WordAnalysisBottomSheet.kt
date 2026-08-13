package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.Ayah
import com.example.ui.theme.Quran_Font

@OptIn(ExperimentalMaterial3Api::class)
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

    ModalBottomSheet(onDismissRequest = { 
        viewModel.clearSearch()
        onDismissRequest() 
    }) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "تحليل الكلمة: $word",
                fontSize = 24.sp,
                fontFamily = Quran_Font,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            TabRow(selectedTabIndex = activeTab) {
                Tab(selected = activeTab == 0, onClick = { activeTab = 0 }) {
                    Text("المتشابهات", modifier = Modifier.padding(16.dp))
                }
                Tab(selected = activeTab == 1, onClick = { activeTab = 1 }) {
                    Text("تفكيك الحروف", modifier = Modifier.padding(16.dp))
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))

            if (activeTab == 0) {
                // المتشابهات
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { 
                        searchQuery = it 
                        viewModel.searchSimilarAyahs(it)
                    },
                    label = { Text("بحث عن الكلمة الخطأ (المتشابهة)") },
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
                                        errorType = "تغيير كلمة بكلمة أخرى (متشابهات)",
                                        readText = searchQuery,
                                        linkedAyahId = resultAyah.numberInSurah // Just simple link for now
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
                Text("تفكيك الحروف والتشكيل", color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(modifier = Modifier.height(8.dp))
                
                // Splitting word into characters (simple approach)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center
                ) {
                    word.forEachIndexed { index, char ->
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier
                                .padding(4.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                                .clickable {
                                    viewModel.logError(ayah, word, "خطأ في التشكيل", charIndex = index)
                                    onDismissRequest()
                                }
                                .padding(8.dp)
                        ) {
                            Text(text = char.toString(), fontFamily = Quran_Font, fontSize = 28.sp)
                            Row(modifier = Modifier.padding(top = 4.dp)) {
                                Icon(Icons.Default.Edit, contentDescription = "تغيير", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Default.Add, contentDescription = "إضافة", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Default.Close, contentDescription = "حذف", modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.error)
                            }
                        }
                    }
                }
            }
        }
    }
}
