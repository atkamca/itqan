import re

with open('app/src/main/java/com/example/data/QuranData.kt', 'r') as f:
    code = f.read()

old_content = """    fun removeTashkeel(text: String): String {
        return text.replace(Regex("[\\u0610-\\u061A\\u064B-\\u065F\\u0670\\u06D6-\\u06ED]"), "")
    }

    fun normalizeArabic(text: String): String {
        return removeTashkeel(text)
            .replace("[أإآٱ]".toRegex(), "ا")
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
    }"""

new_content = """    fun searchAyahs(context: android.content.Context, query: String): List<Ayah> {
        if (allAyahs == null) {
            loadAllAyahs(context)
        }
        if (query.isBlank()) return emptyList()
        val normalizedQuery = query.normalizeQuranText().trim()
        
        return allAyahs?.filter { 
            val normalizedText = it.text.normalizeQuranText()
            normalizedText.contains(normalizedQuery)
        }?.take(5) ?: emptyList()
    }"""

extension_function = """
fun String.normalizeQuranText(): String {
    return this
        // 1. Convert specific letters and diacritics before they get stripped
        .replace("\\u0670", "ا") // الألف الخنجرية
        .replace("\\u0671", "ا") // ألف الوصل
        .replace("آ", "ا") // الألف الممدودة
        .replace("أ", "ا") // همزة قطع
        .replace("إ", "ا") // همزة قطع
        .replace("ٱ", "ا") // ألف وصل أخرى إن وجدت
        .replace("ى", "ي") // الياء المقصورة
        .replace("\\u06E2", "ي") // الياء الصغيرة
        .replace("ؤ", "و")
        .replace("ئ", "ي")
        .replace("ة", "ه")
        // 2. Remove signs (Sila etc)
        .replace("\\u06E5", "") // الواو الصغيرة / صلة صغرى
        .replace("\\u06E6", "") // الياء الصغيرة / صلة
        // 3. Remove all Tashkeel
        .replace(Regex("[\\\\u0610-\\\\u061A\\\\u064B-\\\\u065F\\\\u06D6-\\\\u06ED]"), "")
}

object QuranData {"""

code = code.replace(old_content, new_content)
code = code.replace("object QuranData {", extension_function)

with open('app/src/main/java/com/example/data/QuranData.kt', 'w') as f:
    f.write(code)

print("QuranData updated.")
