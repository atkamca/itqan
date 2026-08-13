package com.example.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.AppDatabase
import com.example.data.Ayah
import com.example.data.ErrorLogEntity
import com.example.data.QuranData
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val dao = AppDatabase.getDatabase(application).errorLogDao()

    val errorLogs: StateFlow<List<ErrorLogEntity>> = dao.getAllLogs()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    private val _selectedSurahId = MutableStateFlow(1)
    val selectedSurahId: StateFlow<Int> = _selectedSurahId.asStateFlow()

    val currentAyahs: StateFlow<List<Ayah>> = _selectedSurahId.map { surahId ->
        QuranData.getAyahsForSurah(application, surahId)
    }.stateIn(viewModelScope, SharingStarted.Lazily, QuranData.getAyahsForSurah(application, 1))

    private val _jumpToAyahIndex = MutableStateFlow(-1)
    val jumpToAyahIndex: StateFlow<Int> = _jumpToAyahIndex.asStateFlow()

    fun selectSurah(surahId: Int) {
        if (_selectedSurahId.value != surahId) {
            _selectedSurahId.value = surahId
            _jumpToAyahIndex.value = 0
        }
    }

    fun jumpToAyah(ayahNumber: Int) {
        val ayahs = currentAyahs.value
        val index = ayahs.indexOfFirst { it.numberInSurah == ayahNumber }
        if (index != -1) {
            _jumpToAyahIndex.value = index
        }
    }
    
    fun resetJumpIndex() {
        _jumpToAyahIndex.value = -1
    }

    fun logError(ayah: Ayah, wordText: String, errorType: String, readText: String? = null, charIndex: Int? = null) {
        viewModelScope.launch {
            dao.insertLog(
                ErrorLogEntity(
                    surahId = ayah.surahId,
                    surahName = ayah.surahName,
                    ayahNumber = ayah.numberInSurah,
                    wordText = wordText,
                    errorType = errorType,
                    readText = readText,
                    charIndex = charIndex,
                    timestamp = System.currentTimeMillis()
                )
            )
        }
    }

    fun clearLogs() {
        viewModelScope.launch {
            dao.clearAll()
        }
    }
}
