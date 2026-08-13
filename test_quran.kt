import java.io.File

fun main() {
    val text = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
    val query = "ٱلرَّحْمَٰنِ"
    
    fun removeTashkeel(t: String): String {
        return t.replace(Regex("[\\u0617-\\u061A\\u064B-\\u0652\\u0670]"), "")
    }
    fun normalizeArabic(t: String): String {
        return removeTashkeel(t)
            .replace(Regex("[أإآٱ]"), "ا")
            .replace("ة", "ه")
            .replace("ى", "ي")
            .replace("ؤ", "و")
            .replace("ئ", "ي")
    }
    
    println(normalizeArabic(text))
    println(normalizeArabic(query))
}
