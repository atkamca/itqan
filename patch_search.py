with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

old_s = '    var searchQuery by remember { mutableStateOf("") }\n    val searchResults by viewModel.searchResults.collectAsStateWithLifecycle()\n    var activeTab by remember { mutableIntStateOf(0) }\n    val isAyahMode = word == "[الآية]"'

new_s = '    val isAyahMode = word == "[الآية]"\n    var searchQuery by remember { mutableStateOf(if (isAyahMode) "" else word) }\n    val searchResults by viewModel.searchResults.collectAsStateWithLifecycle()\n    var activeTab by remember { mutableIntStateOf(0) }\n    \n    LaunchedEffect(word) {\n        if (!isAyahMode) {\n            viewModel.searchSimilarAyahs(word)\n        }\n    }'

if old_s in code:
    code = code.replace(old_s, new_s)
    with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
        f.write(code)
    print("Replaced successfully")
else:
    print("Not found")
