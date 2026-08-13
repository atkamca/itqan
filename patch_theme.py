import os

color_kt = """package com.example.ui.theme

import androidx.compose.ui.graphics.Color

// Premium Islamic Palette
val EmeraldPrimary = Color(0xFF047857)
val EmeraldSecondary = Color(0xFF10B981)
val EmeraldTertiary = Color(0xFF059669)

val GoldAccent = Color(0xFFD97706)
val GoldAccentVariant = Color(0xFFF59E0B)

// Light Mode - Warm Beige/Paper
val BeigeBackground = Color(0xFFFAFAF9) // Very light warm off-white (Paper)
val BeigeSurface = Color(0xFFFFFFFF) // White cards
val BeigeSurfaceVariant = Color(0xFFF4F1EA)

// Dark Mode - Deep Forest / Olive
val OliveBackground = Color(0xFF0F172A) // Very dark blue/green slate
val OliveSurface = Color(0xFF1E293B) // Slate surface
val OliveSurfaceVariant = Color(0xFF334155)

// Accents & Texts
val TextDark = Color(0xFF0F172A)
val TextLight = Color(0xFFF8FAFC)

// Alert Colors
val ErrorLight = Color(0xFFDC2626)
val ErrorDark = Color(0xFFF87171)
val ErrorContainerLight = Color(0xFFFEE2E2)
val ErrorContainerDark = Color(0xFF991B1B)
"""

theme_kt = """package com.example.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val LightColorScheme = lightColorScheme(
    primary = EmeraldPrimary,
    onPrimary = androidx.compose.ui.graphics.Color.White,
    primaryContainer = EmeraldSecondary.copy(alpha = 0.1f),
    onPrimaryContainer = EmeraldPrimary,
    secondary = GoldAccent,
    onSecondary = androidx.compose.ui.graphics.Color.White,
    secondaryContainer = GoldAccentVariant.copy(alpha = 0.15f),
    onSecondaryContainer = GoldAccent,
    tertiary = EmeraldTertiary,
    background = BeigeBackground,
    onBackground = TextDark,
    surface = BeigeSurface,
    onSurface = TextDark,
    surfaceVariant = BeigeSurfaceVariant,
    onSurfaceVariant = TextDark.copy(alpha = 0.8f),
    error = ErrorLight,
    errorContainer = ErrorContainerLight,
    onErrorContainer = ErrorLight
)

private val DarkColorScheme = darkColorScheme(
    primary = EmeraldSecondary,
    onPrimary = OliveBackground,
    primaryContainer = EmeraldPrimary.copy(alpha = 0.3f),
    onPrimaryContainer = EmeraldSecondary,
    secondary = GoldAccentVariant,
    onSecondary = OliveBackground,
    secondaryContainer = GoldAccent.copy(alpha = 0.3f),
    onSecondaryContainer = GoldAccentVariant,
    tertiary = EmeraldTertiary,
    background = OliveBackground,
    onBackground = TextLight,
    surface = OliveSurface,
    onSurface = TextLight,
    surfaceVariant = OliveSurfaceVariant,
    onSurfaceVariant = TextLight.copy(alpha = 0.9f),
    error = ErrorDark,
    errorContainer = ErrorContainerDark,
    onErrorContainer = ErrorDark
)

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as? Activity)?.window
            if (window != null) {
                window.statusBarColor = androidx.compose.ui.graphics.Color.Transparent.toArgb()
                WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
                WindowCompat.setDecorFitsSystemWindows(window, false)
            }
        }
    }
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
"""

type_kt = """package com.example.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.example.R

val UI_Font = FontFamily(
    Font(R.font.cairo_regular, FontWeight.Normal),
    Font(R.font.cairo_bold, FontWeight.Bold)
)
val Quran_Font = FontFamily(
    Font(R.font.amiri_regular, FontWeight.Normal)
)

val Typography = Typography(
    displayLarge = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Bold,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp
    ),
    displayMedium = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Bold,
        fontSize = 45.sp,
        lineHeight = 52.sp,
        letterSpacing = 0.sp
    ),
    headlineLarge = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Bold,
        fontSize = 32.sp,
        lineHeight = 40.sp,
        letterSpacing = 0.sp
    ),
    headlineMedium = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Bold,
        fontSize = 28.sp,
        lineHeight = 36.sp,
        letterSpacing = 0.sp
    ),
    titleLarge = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Bold,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.sp
    ),
    titleMedium = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Bold,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.15.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.25.sp
    ),
    labelLarge = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    ),
    labelMedium = TextStyle(
        fontFamily = UI_Font,
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
    )
)
"""

with open('app/src/main/java/com/example/ui/theme/Color.kt', 'w') as f:
    f.write(color_kt)
with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'w') as f:
    f.write(theme_kt)
with open('app/src/main/java/com/example/ui/theme/Type.kt', 'w') as f:
    f.write(type_kt)

print("Theme updated successfully!")
