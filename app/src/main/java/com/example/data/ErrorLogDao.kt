package com.example.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface ErrorLogDao {
    @Query("SELECT * FROM error_logs ORDER BY timestamp DESC")
    fun getAllLogs(): Flow<List<ErrorLogEntity>>

    @Insert
    suspend fun insertLog(log: ErrorLogEntity)

    @Query("DELETE FROM error_logs")
    suspend fun clearAll()

    @Query("DELETE FROM error_logs WHERE id = (SELECT id FROM error_logs ORDER BY timestamp DESC LIMIT 1)")
    suspend fun deleteLatestLog()
}
