package com.example.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.AppDatabase
import com.example.data.Ayah
import com.example.data.ErrorLogEntity
import com.example.data.QuranData
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val dao = AppDatabase.getDatabase(application).errorLogDao()
    
    val errorLogs: StateFlow<List<ErrorLogEntity>> = dao.getAllLogs()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    private val _selectedSurahId = MutableStateFlow(1)
    val selectedSurahId: StateFlow<Int> = _selectedSurahId.asStateFlow()

    private val _currentAyahs = MutableStateFlow<List<Ayah>>(emptyList())
    val currentAyahs: StateFlow<List<Ayah>> = _currentAyahs.asStateFlow()

    private val _jumpToAyahIndex = MutableStateFlow(-1)
    val jumpToAyahIndex: StateFlow<Int> = _jumpToAyahIndex.asStateFlow()

    private val _searchResults = MutableStateFlow<List<Ayah>>(emptyList())
    val searchResults: StateFlow<List<Ayah>> = _searchResults.asStateFlow()

    private val _snackbarMessage = MutableStateFlow<String?>(null)
    val snackbarMessage: StateFlow<String?> = _snackbarMessage.asStateFlow()

    fun clearSnackbar() {
        _snackbarMessage.value = null
    }

    fun undoLastError() {
        viewModelScope.launch(Dispatchers.IO) {
            dao.deleteLatestLog()
        }
    }

    init {
        loadSurahData(1)
    }

    fun selectSurah(surahId: Int) {
        if (_selectedSurahId.value != surahId) {
            _selectedSurahId.value = surahId
            _jumpToAyahIndex.value = 0
            loadSurahData(surahId)
        }
    }

    private fun loadSurahData(surahId: Int) {
        viewModelScope.launch {
            val ayahs = withContext(Dispatchers.IO) {
                QuranData.getAyahsForSurah(getApplication(), surahId)
            }
            _currentAyahs.value = ayahs
        }
    }

    fun jumpToAyah(ayahNumber: Int) {
        val ayahs = _currentAyahs.value
        val index = ayahs.indexOfFirst { it.numberInSurah == ayahNumber }
        if (index != -1) {
            _jumpToAyahIndex.value = index
        }
    }
    
    fun resetJumpIndex() {
        _jumpToAyahIndex.value = -1
    }

    fun searchSimilarAyahs(query: String) {
        viewModelScope.launch {
            if (query.length < 2) {
                _searchResults.value = emptyList()
                return@launch
            }
            val results = withContext(Dispatchers.IO) {
                QuranData.searchAyahs(getApplication(), query)
            }
            _searchResults.value = results
        }
    }

    fun clearSearch() {
        _searchResults.value = emptyList()
    }

    fun logError(
        ayah: Ayah, 
        wordText: String, 
        errorType: String, 
        readText: String? = null, 
        charIndex: Int? = null,
        linkedAyahId: Int? = null
    ) {
        // Calculate weight based on rules
        val weight = when {
            errorType.contains("تردد") || errorType.contains("شك") -> -5
            errorType.contains("تشكيل") || errorType.contains("حرف") -> -10
            errorType.contains("نسيان") || errorType.contains("متشابه") || errorType.contains("توقف") -> -20
            else -> -10
        }

        viewModelScope.launch(Dispatchers.IO) {
            dao.insertLog(
                ErrorLogEntity(
                    surahId = ayah.surahId,
                    surahName = ayah.surahName,
                    ayahNumber = ayah.numberInSurah,
                    wordText = wordText,
                    errorType = errorType,
                    readText = readText,
                    charIndex = charIndex,
                    errorWeight = weight,
                    linkedAyahId = linkedAyahId,
                    timestamp = System.currentTimeMillis()
                )
            )
            _snackbarMessage.value = "تم تسجيل: $errorType"
        }
    }

    fun clearLogs() {
        viewModelScope.launch(Dispatchers.IO) {
            dao.clearAll()
        }
    }
}
