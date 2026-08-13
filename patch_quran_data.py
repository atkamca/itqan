import re

with open('/app/applet/app/src/main/java/com/example/data/QuranData.kt', 'r') as f:
    code = f.read()

fuzzy_search_logic = """
    fun removeTashkeel(text: String): String {
        return text.replace(Regex("[\\\\u0617-\\\\u061A\\\\u064B-\\\\u0652\\\\u0670]"), "")
    }

    fun normalizeArabic(text: String): String {
        return removeTashkeel(text)
            .replace("[أإآ]".toRegex(), "ا")
            .replace("ة", "ه")
            .replace("ى", "ي")
            .replace("ؤ", "و")
            .replace("ئ", "ي")
    }

    fun searchAyahs(context: android.content.Context, query: String): List<Ayah> {
        if (allAyahs == null) {
            loadAllAyahs(context)
        }
        if (query.isBlank()) return emptyList()
        val normalizedQuery = normalizeArabic(query).trim()
        
        return allAyahs?.filter { 
            val normalizedText = normalizeArabic(it.text)
            normalizedText.contains(normalizedQuery)
        }?.take(5) ?: emptyList()
    }
"""

start_search = code.find("fun searchAyahs(")
end_search = code.find("private fun loadAllAyahs", start_search)
code = code[:start_search] + fuzzy_search_logic + "\n    " + code[end_search:]

with open('/app/applet/app/src/main/java/com/example/data/QuranData.kt', 'w') as f:
    f.write(code)
