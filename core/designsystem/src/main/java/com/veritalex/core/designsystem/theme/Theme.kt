package com.veritalex.core.designsystem.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

enum class AppAppearance { System, Light, Dark }
enum class AppColorSource { Brand, Dynamic }

@Composable
fun VeritalexTheme(
    appearance: AppAppearance = AppAppearance.System,
    colorSource: AppColorSource = AppColorSource.Brand,
    content: @Composable () -> Unit,
) {
    val darkTheme = when (appearance) {
        AppAppearance.System -> isSystemInDarkTheme()
        AppAppearance.Light -> false
        AppAppearance.Dark -> true
    }
    val context = LocalContext.current
    val colors = if (colorSource == AppColorSource.Dynamic && Build.VERSION.SDK_INT >= 31) {
        if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
    } else {
        if (darkTheme) DarkColorScheme else LightColorScheme
    }
    MaterialTheme(
        colorScheme = colors,
        typography = AppTypography,
        shapes = VeritalexShapes,
        content = content,
    )
}
