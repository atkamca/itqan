package com.example.ui.theme

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
    primaryContainer = EmeraldSecondary.copy(alpha = 0.2f),
    onPrimaryContainer = EmeraldPrimary,
    secondary = EmeraldSecondary,
    onSecondary = androidx.compose.ui.graphics.Color.White,
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
    primaryContainer = EmeraldPrimary.copy(alpha = 0.4f),
    onPrimaryContainer = EmeraldSecondary,
    secondary = EmeraldSecondary,
    onSecondary = OliveBackground,
    tertiary = EmeraldTertiary,
    background = OliveBackground,
    onBackground = TextLight,
    surface = OliveSurface,
    onSurface = TextLight,
    surfaceVariant = OliveSurfaceVariant,
    onSurfaceVariant = TextLight.copy(alpha = 0.8f),
    error = ErrorDark,
    errorContainer = ErrorContainerDark,
    onErrorContainer = ErrorDark
)

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false, // Set to false to force our custom colors instead of Material You
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
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.background.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
