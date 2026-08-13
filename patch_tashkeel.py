import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

# Replace LaunchedEffect block to search normalized word, and searchQuery to be normalized.
old_search_block = """    val isAyahMode = word == "[الآية]"
    var searchQuery by remember { mutableStateOf(if (isAyahMode) "" else word) }
    val searchResults by viewModel.searchResults.collectAsStateWithLifecycle()
    var activeTab by remember { mutableIntStateOf(0) }
    
    LaunchedEffect(word) {
        if (!isAyahMode) {
            viewModel.searchSimilarAyahs(word)
        }
    }"""

new_search_block = """    val isAyahMode = word == "[الآية]"
    val normalizedWord = remember(word) { com.example.data.QuranData.normalizeArabic(word) }
    var searchQuery by remember { mutableStateOf(if (isAyahMode) "" else normalizedWord) }
    val searchResults by viewModel.searchResults.collectAsStateWithLifecycle()
    var activeTab by remember { mutableIntStateOf(0) }
    
    LaunchedEffect(word) {
        if (!isAyahMode) {
            viewModel.searchSimilarAyahs(normalizedWord)
        }
    }"""

if old_search_block in code:
    code = code.replace(old_search_block, new_search_block)
    with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
        f.write(code)
    print("Replaced successfully")
else:
    print("Could not find old_search_block")
