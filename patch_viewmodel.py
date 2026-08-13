import re

with open('/app/applet/app/src/main/java/com/example/ui/MainViewModel.kt', 'r') as f:
    code = f.read()

props_insert = """    private val _searchResults = MutableStateFlow<List<Ayah>>(emptyList())
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
"""
code = code.replace("    private val _searchResults = MutableStateFlow<List<Ayah>>(emptyList())\n    val searchResults: StateFlow<List<Ayah>> = _searchResults.asStateFlow()\n", props_insert)

# Update logError to show snackbar
log_error_old = """                    timestamp = System.currentTimeMillis()
                )
            )
        }
    }"""
log_error_new = """                    timestamp = System.currentTimeMillis()
                )
            )
            _snackbarMessage.value = "تم تسجيل: $errorType"
        }
    }"""
code = code.replace(log_error_old, log_error_new)

with open('/app/applet/app/src/main/java/com/example/ui/MainViewModel.kt', 'w') as f:
    f.write(code)
