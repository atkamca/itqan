import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

# Replace DropdownMenu with an AlertDialog for selection
flow_row_old = """                            DropdownMenu(
                                expanded = showAddMenuForIndex == index,
                                onDismissRequest = { showAddMenuForIndex = null }
                            ) {
                                DropdownMenuItem(
                                    text = { Text("أضفنا مد") },
                                    onClick = {
                                        // To keep it simple in UI, log it with a generic message, or we could open a secondary dial.
                                        // We will just log "زيادة مد" for now as it captures the semantic meaning perfectly.
                                        viewModel.logError(ayah, word, "زيادة مد (ا، و، ي)", charIndex = index)
                                        showAddMenuForIndex = null
                                        onDismissRequest()
                                    }
                                )
                                DropdownMenuItem(
                                    text = { Text("أضفنا حرف") },
                                    onClick = {
                                        viewModel.logError(ayah, word, "زيادة حرف", charIndex = index)
                                        showAddMenuForIndex = null
                                        onDismissRequest()
                                    }
                                )
                            }"""

flow_row_new = """                            if (showAddMenuForIndex == index) {
                                var step by remember { mutableIntStateOf(1) } // 1: Choose type, 2: Choose letter
                                var isMadd by remember { mutableStateOf(true) }
                                
                                AlertDialog(
                                    onDismissRequest = { showAddMenuForIndex = null },
                                    title = { Text(if (step == 1) "ماذا أضفت بالخطأ؟" else if (isMadd) "اختر حرف المد" else "اختر الحرف") },
                                    text = {
                                        if (step == 1) {
                                            Column {
                                                TextButton(onClick = { isMadd = true; step = 2 }, modifier = Modifier.fillMaxWidth()) { Text("أضفنا مد") }
                                                TextButton(onClick = { isMadd = false; step = 2 }, modifier = Modifier.fillMaxWidth()) { Text("أضفنا حرف") }
                                            }
                                        } else {
                                            val options = if (isMadd) listOf("ا", "و", "ي", "ى") else listOf("س", "ص", "ض", "ظ", "ذ", "ز", "ت", "ط", "ق", "ك", "ح", "خ", "ه", "ء")
                                            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                                options.forEach { opt ->
                                                    Box(
                                                        modifier = Modifier
                                                            .size(40.dp)
                                                            .clip(CircleShape)
                                                            .background(MaterialTheme.colorScheme.primaryContainer)
                                                            .clickable {
                                                                viewModel.logError(ayah, word, "زيادة ${if (isMadd) "مد" else "حرف"} ($opt)", charIndex = index)
                                                                showAddMenuForIndex = null
                                                                onDismissRequest()
                                                            },
                                                        contentAlignment = Alignment.Center
                                                    ) {
                                                        Text(text = opt, fontSize = 24.sp)
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    confirmButton = {
                                        TextButton(onClick = { showAddMenuForIndex = null }) {
                                            Text("إلغاء")
                                        }
                                    }
                                )
                            }"""
code = code.replace(flow_row_old, flow_row_new)

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)
