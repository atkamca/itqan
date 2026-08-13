import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    code = f.read()

# Make the card beautiful
old_card = """Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {"""

new_card = """Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
                        shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp)
                    ) {
                        Row(modifier = Modifier.fillMaxWidth().height(IntrinsicSize.Min)) {
                            // Colored side-bar based on error type
                            Box(
                                modifier = Modifier
                                    .width(6.dp)
                                    .fillMaxHeight()
                                    .background(getErrorColor(log.errorType, MaterialTheme.colorScheme.primary))
                            )
                            Column(modifier = Modifier.padding(16.dp).weight(1f)) {"""

code = code.replace(old_card, new_card)

# Close the Row added in ReportsScreen
old_column_end = """if (!log.readText.isNullOrEmpty()) {
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(text = "تمت قراءتها: ${log.readText}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                            }
                        }
                    }"""

new_column_end = """if (!log.readText.isNullOrEmpty()) {
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(text = "تمت قراءتها: ${log.readText}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                            }
                        }
                        }
                    }"""

code = code.replace(old_column_end, new_column_end)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(code)

print("Updated Reports Screen Cards")
