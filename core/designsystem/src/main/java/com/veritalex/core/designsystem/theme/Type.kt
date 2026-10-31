package com.veritalex.core.designsystem.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.veritalex.core.designsystem.R

private val InterfaceFontFamily = FontFamily(
    Font(R.font.roboto_flex, FontWeight.Normal),
    Font(R.font.roboto_flex, FontWeight.Medium),
    Font(R.font.roboto_flex, FontWeight.SemiBold),
    Font(R.font.roboto_flex, FontWeight.Bold),
)

private val baseline = Typography()

internal val AppTypography = Typography(
    displayLarge = baseline.displayLarge.copy(fontFamily = InterfaceFontFamily),
    displayMedium = baseline.displayMedium.copy(fontFamily = InterfaceFontFamily),
    displaySmall = baseline.displaySmall.copy(fontFamily = InterfaceFontFamily),
    headlineLarge = baseline.headlineLarge.copy(fontFamily = InterfaceFontFamily),
    headlineMedium = baseline.headlineMedium.copy(fontFamily = InterfaceFontFamily),
    headlineSmall = baseline.headlineSmall.copy(
        fontFamily = InterfaceFontFamily, fontWeight = FontWeight.Medium,
        fontSize = 24.sp, lineHeight = 32.sp,
    ),
    titleLarge = TextStyle(
        fontFamily = InterfaceFontFamily, fontWeight = FontWeight.Medium,
        fontSize = 24.sp, lineHeight = 32.sp,
    ),
    titleMedium = TextStyle(
        fontFamily = InterfaceFontFamily, fontWeight = FontWeight.Medium,
        fontSize = 20.sp, lineHeight = 28.sp,
    ),
    titleSmall = TextStyle(
        fontFamily = InterfaceFontFamily, fontWeight = FontWeight.Medium,
        fontSize = 16.sp, lineHeight = 24.sp,
    ),
    bodyLarge = TextStyle(fontFamily = InterfaceFontFamily, fontSize = 16.sp, lineHeight = 24.sp),
    bodyMedium = TextStyle(fontFamily = InterfaceFontFamily, fontSize = 14.sp, lineHeight = 20.sp),
    bodySmall = baseline.bodySmall.copy(fontFamily = InterfaceFontFamily),
    labelLarge = TextStyle(
        fontFamily = InterfaceFontFamily, fontWeight = FontWeight.Medium,
        fontSize = 14.sp, lineHeight = 20.sp,
    ),
    labelMedium = baseline.labelMedium.copy(fontFamily = InterfaceFontFamily),
    labelSmall = baseline.labelSmall.copy(fontFamily = InterfaceFontFamily),
)
