import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

# Update FlowRow inside WordAnalysisBottomSheet to use onReplaceLetter and Add popup
flow_row_old = """                FlowRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    letters.forEachIndexed { index, charChunk ->
                        InteractiveLetterBox(
                            charChunk = charChunk,
                            onDiacriticChange = { 
                                viewModel.logError(ayah, word, "خطأ في التشكيل", charIndex = index)
                                onDismissRequest()
                            },
                            onDelete = {
                                viewModel.logError(ayah, word, "زيادة حرف", charIndex = index)
                                onDismissRequest()
                            }
                        )
                        
                        if (index < letters.size - 1) {
                            Box(
                                modifier = Modifier
                                    .width(20.dp)
                                    .height(60.dp)
                                    .clickable {
                                        viewModel.logError(ayah, word, "نقصان حرف", charIndex = index)
                                        onDismissRequest()
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Add, contentDescription = "Add", tint = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f), modifier = Modifier.size(16.dp))
                            }
                        }
                    }
                }"""

flow_row_new = """                var showAddMenuForIndex by remember { mutableStateOf<Int?>(null) }
                FlowRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    letters.forEachIndexed { index, charChunk ->
                        InteractiveLetterBox(
                            charChunk = charChunk,
                            onDiacriticChange = { 
                                viewModel.logError(ayah, word, "خطأ في التشكيل", charIndex = index)
                                onDismissRequest()
                            },
                            onDelete = {
                                viewModel.logError(ayah, word, "حذف الحرف / المد", charIndex = index)
                                onDismissRequest()
                            },
                            onReplaceLetter = {
                                viewModel.logError(ayah, word, "تغيير الحرف / المد", charIndex = index)
                                onDismissRequest()
                            }
                        )
                        
                        Box(
                            modifier = Modifier
                                .width(20.dp)
                                .height(60.dp)
                                .clickable {
                                    showAddMenuForIndex = index
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Add", tint = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f), modifier = Modifier.size(16.dp))
                            
                            DropdownMenu(
                                expanded = showAddMenuForIndex == index,
                                onDismissRequest = { showAddMenuForIndex = null }
                            ) {
                                DropdownMenuItem(
                                    text = { Text("أضفنا مد") },
                                    onClick = {
                                        viewModel.logError(ayah, word, "زيادة مد", charIndex = index)
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
                            }
                        }
                    }
                }"""
code = code.replace(flow_row_old, flow_row_new)

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)
