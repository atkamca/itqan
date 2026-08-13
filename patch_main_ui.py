import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# 1. Update MorakebApp
morakeb_app_regex = r"@Composable\nfun MorakebApp\(viewModel: MainViewModel\) \{.*?(?=@OptIn\(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class, ExperimentalLayoutApi::class\)\n@Composable\nfun ReadingScreen)"
new_morakeb_app = """@OptIn(androidx.compose.animation.ExperimentalAnimationApi::class)
@Composable
fun MorakebApp(viewModel: MainViewModel) {
    var selectedTab by remember { mutableIntStateOf(0) }
    val snackbarHostState = remember { SnackbarHostState() }
    val snackbarMessage by viewModel.snackbarMessage.collectAsStateWithLifecycle()

    LaunchedEffect(snackbarMessage) {
        snackbarMessage?.let { msg ->
            val result = snackbarHostState.showSnackbar(
                message = msg,
                actionLabel = "تراجع",
                duration = SnackbarDuration.Short
            )
            if (result == SnackbarResult.ActionPerformed) {
                viewModel.undoLastError()
            }
            viewModel.clearSnackbar()
        }
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        bottomBar = {
            androidx.compose.material3.Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .navigationBarsPadding()
                    .padding(horizontal = 24.dp, vertical = 16.dp),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(32.dp),
                shadowElevation = 12.dp,
                color = MaterialTheme.colorScheme.surface.copy(alpha = 0.9f),
            ) {
                NavigationBar(
                    containerColor = androidx.compose.ui.graphics.Color.Transparent,
                    tonalElevation = 0.dp,
                    windowInsets = WindowInsets(0, 0, 0, 0)
                ) {
                    NavigationBarItem(
                        icon = { Icon(Icons.AutoMirrored.Filled.MenuBook, contentDescription = "المراجعة") },
                        label = { Text("المراجعة", fontWeight = FontWeight.Bold, fontFamily = com.example.ui.theme.UI_Font) },
                        selected = selectedTab == 0,
                        onClick = { selectedTab = 0 },
                        colors = NavigationBarItemDefaults.colors(
                            indicatorColor = MaterialTheme.colorScheme.primaryContainer,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Filled.Analytics, contentDescription = "التقارير") },
                        label = { Text("التقارير", fontWeight = FontWeight.Bold, fontFamily = com.example.ui.theme.UI_Font) },
                        selected = selectedTab == 1,
                        onClick = { selectedTab = 1 },
                        colors = NavigationBarItemDefaults.colors(
                            indicatorColor = MaterialTheme.colorScheme.primaryContainer,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    )
                }
            }
        },
        containerColor = MaterialTheme.colorScheme.background
    ) { innerPadding ->
        androidx.compose.animation.AnimatedContent(
            targetState = selectedTab,
            modifier = Modifier.padding(innerPadding).fillMaxSize(),
            transitionSpec = {
                androidx.compose.animation.fadeIn() androidx.compose.animation.togetherWith androidx.compose.animation.fadeOut()
            }
        ) { targetTab ->
            if (targetTab == 0) {
                ReadingScreen(viewModel)
            } else {
                ReportsScreen(viewModel)
            }
        }
    }
}

"""

code = re.sub(morakeb_app_regex, new_morakeb_app, code, flags=re.DOTALL)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)

print("Updated MorakebApp")
