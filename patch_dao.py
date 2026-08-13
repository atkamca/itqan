import re

with open('/app/applet/app/src/main/java/com/example/data/ErrorLogDao.kt', 'r') as f:
    code = f.read()

dao_insert = """    @Query("DELETE FROM error_logs")
    suspend fun clearAll()

    @Query("DELETE FROM error_logs WHERE id = (SELECT id FROM error_logs ORDER BY timestamp DESC LIMIT 1)")
    suspend fun deleteLatestLog()"""
code = code.replace("    @Query(\"DELETE FROM error_logs\")\n    suspend fun clearAll()", dao_insert)

with open('/app/applet/app/src/main/java/com/example/data/ErrorLogDao.kt', 'w') as f:
    f.write(code)
