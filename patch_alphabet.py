import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

# Replace similarLetters in InteractiveLetterBox
old_similar = 'val similarLetters = listOf("س", "ص", "ض", "ظ", "ذ", "ز", "ت", "ط", "ق", "ك", "ح", "خ", "ه", "ء", "ا", "و", "ي")'
new_similar = 'val similarLetters = listOf("ا", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "ه", "و", "ي", "ء", "ى", "ة")'
code = code.replace(old_similar, new_similar)

# Replace options in Add Menu
old_options = 'val options = if (isMadd) listOf("ا", "و", "ي", "ى") else listOf("س", "ص", "ض", "ظ", "ذ", "ز", "ت", "ط", "ق", "ك", "ح", "خ", "ه", "ء")'
new_options = 'val options = if (isMadd) listOf("ا", "و", "ي", "ى") else listOf("ا", "ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "ه", "و", "ي", "ء", "ى", "ة")'
code = code.replace(old_options, new_options)

# Since AlertDialog with FlowRow might overflow vertically and look bad if it gets too tall, 
# let's add verticalScroll to the FlowRow or wrap it.
old_flow_row = 'FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {'
new_flow_row = 'FlowRow(modifier = Modifier.verticalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {'
code = code.replace(old_flow_row, new_flow_row)


with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)
print("Patched alphabet!")
