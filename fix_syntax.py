import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# Let's fix the experimental FlowRow issue in WordAnalysisBottomSheet.kt
with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    bot_code = f.read()
if "@OptIn(ExperimentalLayoutApi::class)" not in bot_code:
    bot_code = bot_code.replace("fun InteractiveLetterBox(", "@OptIn(ExperimentalLayoutApi::class)\n@Composable\nfun InteractiveLetterBox(")

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(bot_code)
