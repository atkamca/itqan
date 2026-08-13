package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "error_logs")
data class ErrorLogEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val surahId: Int,
    val surahName: String,
    val ayahNumber: Int,
    val wordText: String,
    val errorType: String,
    val readText: String? = null,
    val charIndex: Int? = null,
    val errorWeight: Int = 0,
    val linkedAyahId: Int? = null,
    val timestamp: Long = System.currentTimeMillis()
)
