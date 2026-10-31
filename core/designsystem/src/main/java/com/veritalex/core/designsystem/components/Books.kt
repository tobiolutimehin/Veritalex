package com.veritalex.core.designsystem.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextOverflow
import com.veritalex.core.designsystem.R
import com.veritalex.core.designsystem.theme.ReaderTheme
import com.veritalex.core.designsystem.theme.ReaderTypography
import com.veritalex.core.designsystem.theme.VeritalexLayout
import com.veritalex.core.designsystem.theme.VeritalexSpacing

/** Flat tonal grouping, with the shared 16dp card radius and no persistent shadow. */
@Composable
fun VeritalexCard(modifier: Modifier = Modifier, content: @Composable ColumnScope.() -> Unit) {
    Card(
        modifier = modifier, shape = MaterialTheme.shapes.medium,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLow),
        content = content,
    )
}

/** No image loading or book state. Full metadata must also appear beside/below this small cover. */
@Composable
fun BookCoverFallback(title: String, author: String, modifier: Modifier = Modifier) {
    val description = stringResource(R.string.book_cover_description, title, author)
    Surface(
        modifier = modifier.aspectRatio(2f / 3f).clearAndSetSemantics { contentDescription = description },
        shape = MaterialTheme.shapes.extraSmall,
        color = MaterialTheme.colorScheme.primaryContainer,
        contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
    ) {
        Column(
            modifier = Modifier.padding(VeritalexSpacing.small),
            verticalArrangement = Arrangement.SpaceBetween,
        ) {
            Text(
                title, modifier = Modifier.weight(1f), style = MaterialTheme.typography.labelMedium,
                maxLines = 4, overflow = TextOverflow.Ellipsis,
            )
            Text(author, style = MaterialTheme.typography.labelSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
    }
}

/** A non-interactive row until a real feature supplies an action. Titles reflow without truncation. */
@Composable
fun BookListRow(title: String, author: String, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier.fillMaxWidth().semantics(mergeDescendants = true) {},
        horizontalArrangement = Arrangement.spacedBy(VeritalexSpacing.medium),
    ) {
        // Adjacent metadata already describes the book; do not announce the cover a second time.
        androidx.compose.foundation.layout.Box(Modifier.clearAndSetSemantics {}) {
            BookCoverFallback(title, author, Modifier.width(VeritalexLayout.listCoverWidth))
        }
        Column(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.extraSmall),
        ) {
            Text(title, style = MaterialTheme.typography.titleSmall)
            Text(author, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

/** Visual prose specimen, not a reader or a position-owning component. */
@Composable
fun ReadingPreview(chapter: String, passage: String, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier.widthIn(max = VeritalexLayout.readerMaxWidth),
        shape = MaterialTheme.shapes.medium,
        color = ReaderTheme.colors.background,
        contentColor = ReaderTheme.colors.text,
    ) {
        Column(
            modifier = Modifier.padding(VeritalexSpacing.large),
            verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.medium),
        ) {
            Text(chapter, style = ReaderTypography.chapter, modifier = Modifier.semantics { heading() })
            SelectionContainer { Text(passage, style = ReaderTypography.prose) }
        }
    }
}
