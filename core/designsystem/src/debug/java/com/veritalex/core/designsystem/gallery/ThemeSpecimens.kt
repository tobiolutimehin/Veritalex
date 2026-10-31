package com.veritalex.core.designsystem.gallery

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.dp
import com.veritalex.core.designsystem.components.BookListRow
import com.veritalex.core.designsystem.components.ReadingPreview
import com.veritalex.core.designsystem.components.VeritalexCard
import com.veritalex.core.designsystem.preview.VeritalexLargeTextPreviews
import com.veritalex.core.designsystem.preview.VeritalexThemePreviews
import com.veritalex.core.designsystem.theme.ReaderPaper
import com.veritalex.core.designsystem.theme.ReaderTheme
import com.veritalex.core.designsystem.theme.VeritalexLayout
import com.veritalex.core.designsystem.theme.VeritalexSpacing
import com.veritalex.core.designsystem.theme.VeritalexTheme

@Composable
internal fun ColorSpecimens() {
    val c = MaterialTheme.colorScheme
    GallerySection("Color roles") {
        listOf(
            Triple("Primary / onPrimary", c.primary, c.onPrimary),
            Triple("Primary container", c.primaryContainer, c.onPrimaryContainer),
            Triple("Secondary / onSecondary", c.secondary, c.onSecondary),
            Triple("Secondary container", c.secondaryContainer, c.onSecondaryContainer),
            Triple("Tertiary / onTertiary", c.tertiary, c.onTertiary),
            Triple("Tertiary container", c.tertiaryContainer, c.onTertiaryContainer),
            Triple("Error / onError", c.error, c.onError),
            Triple("Error container", c.errorContainer, c.onErrorContainer),
            Triple("Surface", c.surface, c.onSurface),
            Triple("Container lowest", c.surfaceContainerLowest, c.onSurface),
            Triple("Container low", c.surfaceContainerLow, c.onSurface),
            Triple("Container", c.surfaceContainer, c.onSurface),
            Triple("Container high", c.surfaceContainerHigh, c.onSurface),
            Triple("Container highest", c.surfaceContainerHighest, c.onSurface),
            Triple("Surface dim", c.surfaceDim, c.onSurface),
            Triple("Surface bright", c.surfaceBright, c.onSurface),
            Triple("Inverse surface", c.inverseSurface, c.inverseOnSurface),
            Triple("Primary fixed", c.primaryFixed, c.onPrimaryFixed),
            Triple("Primary fixed dim", c.primaryFixedDim, c.onPrimaryFixedVariant),
            Triple("Secondary fixed", c.secondaryFixed, c.onSecondaryFixed),
            Triple("Secondary fixed dim", c.secondaryFixedDim, c.onSecondaryFixedVariant),
            Triple("Tertiary fixed", c.tertiaryFixed, c.onTertiaryFixed),
            Triple("Tertiary fixed dim", c.tertiaryFixedDim, c.onTertiaryFixedVariant),
        ).forEach { (label, background, foreground) -> Swatch(label, background, foreground) }
        Text("Supporting text uses onSurfaceVariant", color = c.onSurfaceVariant)
        HorizontalDivider(color = c.outline)
        Text("Outline: field and control boundary", style = MaterialTheme.typography.bodyMedium)
        HorizontalDivider(color = c.outlineVariant)
        Text("Outline variant: quiet divider", style = MaterialTheme.typography.bodyMedium)
    }
}

@Composable
private fun Swatch(label: String, background: Color, foreground: Color) {
    Surface(color = background, contentColor = foreground, shape = MaterialTheme.shapes.small, modifier = Modifier.fillMaxWidth()) {
        Text(label, Modifier.padding(VeritalexSpacing.compact), style = MaterialTheme.typography.bodyMedium)
    }
}

@Composable
internal fun TypographySpecimens() {
    val t = MaterialTheme.typography
    GallerySection("Interface type · Roboto Flex") {
        listOf(
            "Display large" to t.displayLarge, "Display medium" to t.displayMedium, "Display small" to t.displaySmall,
            "Headline large" to t.headlineLarge, "Headline medium" to t.headlineMedium, "Headline small" to t.headlineSmall,
            "Title large · screen" to t.titleLarge, "Title medium · section" to t.titleMedium, "Title small · book" to t.titleSmall,
            "Body large · body" to t.bodyLarge, "Body medium · supporting" to t.bodyMedium, "Body small · minor metadata" to t.bodySmall,
            "Label large · action" to t.labelLarge, "Label medium · chip" to t.labelMedium, "Label small · compact metadata" to t.labelSmall,
        ).forEach { (name, style) -> TypeSpecimen(name, style) }
    }
}

@Composable
private fun TypeSpecimen(name: String, style: TextStyle) {
    Text("$name · ${style.fontSize.value.toInt()}/${style.lineHeight.value.toInt()}", style = MaterialTheme.typography.bodySmall)
    Text(if (style.fontSize.value > 24) "Aa" else "A quiet place to read", style = style)
    HorizontalDivider()
}

@Composable
internal fun LayoutSpecimens() {
    GallerySection("Spacing and shape") {
        listOf(VeritalexSpacing.extraSmall, VeritalexSpacing.small, VeritalexSpacing.compact,
            VeritalexSpacing.medium, VeritalexSpacing.large, VeritalexSpacing.extraLarge,
        ).forEach { gap ->
            Row(horizontalArrangement = Arrangement.spacedBy(VeritalexSpacing.medium)) {
                Surface(Modifier.width(gap).height(24.dp), color = MaterialTheme.colorScheme.primary) {}
                Text("${gap.value.toInt()} dp")
            }
        }
        listOf("Cover · 4 dp" to MaterialTheme.shapes.extraSmall,
            "Small control · 8 dp" to MaterialTheme.shapes.small,
            "Card / field · 16 dp" to MaterialTheme.shapes.medium,
            "Large · 24 dp" to MaterialTheme.shapes.large,
            "Sheet / dialog · 28 dp" to MaterialTheme.shapes.extraLarge,
        ).forEach { (label, shape) ->
            Surface(shape = shape, color = MaterialTheme.colorScheme.surfaceContainerHigh, modifier = Modifier.fillMaxWidth()) {
                Text(label, Modifier.padding(VeritalexSpacing.large))
            }
        }
        Text("Buttons are pills. Text-bearing controls grow; touch targets are at least 48 dp. Gutters: ${VeritalexLayout.gutter.value.toInt()} dp in this window.")
    }
}

@Composable
internal fun BookSpecimens() {
    GallerySection("Covers and book rows") {
        BookListRow("Pride and Prejudice", "Jane Austen")
        HorizontalDivider()
        BookListRow("A deliberately long sample book title that reflows across several lines", "An author with a long name for layout review")
        VeritalexCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(VeritalexSpacing.medium)) {
                BookListRow("Frankenstein", "Mary Shelley")
            }
        }
        Text("Covers are typeset fallbacks. These specimens load no images and open no books.", style = MaterialTheme.typography.bodyMedium)
    }
}

@Composable
internal fun ReaderSpecimens() {
    GallerySection("Reader paper · Literata") {
        Text("Paper stays independent when app appearance or wallpaper color changes.")
        ReaderPaper.entries.forEach { paper ->
            Text(paper.name, style = MaterialTheme.typography.titleSmall)
            ReaderTheme(paper) {
                ReadingPreview("Chapter 1", "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.")
                Swatch("Supporting prose metadata", ReaderTheme.colors.background, ReaderTheme.colors.supportingText)
                Swatch("Selected text", ReaderTheme.colors.selection, ReaderTheme.colors.text)
                Swatch("Highlighted passage", ReaderTheme.colors.highlight, ReaderTheme.colors.onHighlight)
            }
        }
    }
}

@VeritalexThemePreviews
@VeritalexLargeTextPreviews
@Composable
private fun ReaderPreview() {
    VeritalexTheme {
        Surface {
            Column(Modifier.verticalScroll(rememberScrollState()).padding(VeritalexSpacing.medium)) { ReaderSpecimens() }
        }
    }
}
