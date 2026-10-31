package com.veritalex.core.designsystem.theme

import androidx.compose.foundation.text.selection.LocalTextSelectionColors
import androidx.compose.foundation.text.selection.TextSelectionColors
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontVariation
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.veritalex.core.designsystem.R

enum class ReaderPaper { Light, Sepia, Dark }

/** Paper is independent of app appearance and wallpaper accents. */
@Immutable
data class ReaderColors(
    val background: Color,
    val text: Color,
    val supportingText: Color,
    val selection: Color,
    val selectionHandle: Color,
    val highlight: Color,
    val onHighlight: Color,
)

fun ReaderPaper.colors(): ReaderColors = when (this) {
    ReaderPaper.Light -> ReaderColors(
        background = Color(0xFFFFF8F3), text = Color(0xFF241A14),
        supportingText = Color(0xFF55483D), selection = Color(0xFFFFDCBF),
        selectionHandle = Color(0xFF895021), highlight = Color(0xFFF6E5A8),
        onHighlight = Color(0xFF241A14),
    )
    ReaderPaper.Sepia -> ReaderColors(
        background = Color(0xFFF4E8D1), text = Color(0xFF302319),
        supportingText = Color(0xFF604E3D), selection = Color(0xFFE6C9A3),
        selectionHandle = Color(0xFF895021), highlight = Color(0xFFEBD998),
        onHighlight = Color(0xFF302319),
    )
    ReaderPaper.Dark -> ReaderColors(
        background = Color(0xFF19120D), text = Color(0xFFF0DFD6),
        supportingText = Color(0xFFD6C3B7), selection = Color(0xFF6D3A0D),
        selectionHandle = Color(0xFFFFB77F), highlight = Color(0xFF5B4A1D),
        onHighlight = Color(0xFFF0DFD6),
    )
}

private val ProseFont = FontFamily(
    Font(R.font.literata, FontWeight.Normal, variationSettings = FontVariation.Settings(FontVariation.weight(400))),
    Font(R.font.literata, FontWeight.Medium, variationSettings = FontVariation.Settings(FontVariation.weight(500))),
)

object ReaderTypography {
    val prose = TextStyle(fontFamily = ProseFont, fontSize = 19.sp, lineHeight = 32.sp)
    val chapter = TextStyle(
        fontFamily = ProseFont, fontWeight = FontWeight.Medium, fontSize = 26.sp, lineHeight = 34.sp,
    )
}

private val LocalReaderColors = staticCompositionLocalOf { ReaderPaper.Light.colors() }

object ReaderTheme {
    val colors: ReaderColors @Composable get() = LocalReaderColors.current
}

@Composable
fun ReaderTheme(paper: ReaderPaper, content: @Composable () -> Unit) {
    val colors = paper.colors()
    CompositionLocalProvider(
        LocalReaderColors provides colors,
        LocalTextSelectionColors provides TextSelectionColors(colors.selectionHandle, colors.selection),
        content = content,
    )
}
