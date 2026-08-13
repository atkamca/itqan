import re

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'r') as f:
    code = f.read()

flow_row_old = """                                DropdownMenuItem(
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
                                )"""

flow_row_new = """                                DropdownMenuItem(
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
                                )"""
code = code.replace(flow_row_old, flow_row_new)

with open('/app/applet/app/src/main/java/com/example/ui/WordAnalysisBottomSheet.kt', 'w') as f:
    f.write(code)
