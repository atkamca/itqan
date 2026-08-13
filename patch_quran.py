import re

with open('/app/applet/app/src/main/java/com/example/data/QuranData.kt', 'r') as f:
    code = f.read()

search_func = """    fun searchAyahs(context: android.content.Context, query: String): List<Ayah> {
        if (allAyahs == null) {
            loadAllAyahs(context)
        }
        val normalizedQuery = query.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه")
        return allAyahs?.filter { 
            val normalizedText = it.text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه")
            normalizedText.contains(normalizedQuery)
        }?.take(10) ?: emptyList()
    }
"""

if "fun searchAyahs" not in code:
    code = code.replace("private fun loadAllAyahs", search_func + "\n    private fun loadAllAyahs")

with open('/app/applet/app/src/main/java/com/example/data/QuranData.kt', 'w') as f:
    f.write(code)
