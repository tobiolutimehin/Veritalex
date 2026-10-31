package com.veritalex.core.designsystem.theme

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import org.junit.Assert.assertTrue
import org.junit.Test

class ContrastTest {
    private fun checkContrast(label: String, foreground: Color, background: Color, minimum: Float = 4.5f) {
        val a = foreground.luminance()
        val b = background.luminance()
        val ratio = (maxOf(a, b) + 0.05f) / (minOf(a, b) + 0.05f)
        assertTrue("$label: contrast $ratio below $minimum", ratio >= minimum)
    }

    @Test fun brandTextAndControlBoundariesHaveSufficientContrast() {
        listOf(LightColorScheme, DarkColorScheme).forEach { c ->
            listOf(
                c.onPrimary to c.primary, c.onPrimaryContainer to c.primaryContainer,
                c.onSecondary to c.secondary, c.onSecondaryContainer to c.secondaryContainer,
                c.onTertiary to c.tertiary, c.onTertiaryContainer to c.tertiaryContainer,
                c.onError to c.error, c.onErrorContainer to c.errorContainer,
                c.inverseOnSurface to c.inverseSurface, c.inversePrimary to c.inverseSurface,
                c.primary to c.surface, c.error to c.surface,
                c.onPrimaryFixed to c.primaryFixed, c.onPrimaryFixedVariant to c.primaryFixedDim,
                c.onSecondaryFixed to c.secondaryFixed, c.onSecondaryFixedVariant to c.secondaryFixedDim,
                c.onTertiaryFixed to c.tertiaryFixed, c.onTertiaryFixedVariant to c.tertiaryFixedDim,
            ).forEachIndexed { i, (fg, bg) -> checkContrast("role $i", fg, bg) }
            listOf(c.surface, c.surfaceContainerLowest, c.surfaceContainerLow, c.surfaceContainer,
                c.surfaceContainerHigh, c.surfaceContainerHighest, c.surfaceBright, c.surfaceDim,
            ).forEach { surface ->
                checkContrast("body", c.onSurface, surface)
                checkContrast("supporting", c.onSurfaceVariant, surface)
            }
            checkContrast("field outline", c.outline, c.surface, 3f)
        }
    }

    @Test fun everyPaperSupportsProseSelectionAndHighlights() {
        ReaderPaper.entries.forEach { paper ->
            val c = paper.colors()
            checkContrast("$paper prose", c.text, c.background)
            checkContrast("$paper supporting", c.supportingText, c.background)
            // Selection keeps the original prose foreground; it must work on both backgrounds.
            checkContrast("$paper selection", c.text, c.selection)
            checkContrast("$paper highlight", c.onHighlight, c.highlight)
            checkContrast("$paper handle", c.selectionHandle, c.background, 3f)
        }
    }
}
