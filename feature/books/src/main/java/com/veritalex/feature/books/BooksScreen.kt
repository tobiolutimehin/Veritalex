package com.veritalex.feature.books

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import com.veritalex.core.designsystem.preview.VeritalexLargeTextPreviews
import com.veritalex.core.designsystem.preview.VeritalexPreviews
import com.veritalex.core.designsystem.preview.VeritalexThemePreviews
import com.veritalex.core.designsystem.theme.VeritalexTheme
import com.veritalex.core.designsystem.components.BookListRow
import com.veritalex.core.designsystem.components.VeritalexMessage
import com.veritalex.core.designsystem.theme.VeritalexLayout
import com.veritalex.core.designsystem.theme.VeritalexSpacing

@Composable
fun BooksScreen(books: List<Book>, modifier: Modifier = Modifier) {
    Box(modifier = modifier.fillMaxSize(), contentAlignment = Alignment.TopCenter) {
        LazyColumn(
            modifier = Modifier.widthIn(max = VeritalexLayout.contentMaxWidth).fillMaxSize(),
            contentPadding = PaddingValues(
                horizontal = VeritalexLayout.gutter,
                vertical = VeritalexSpacing.large,
            ),
            verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.large),
        ) {
            item {
                Column(
                    modifier = Modifier.padding(bottom = VeritalexSpacing.compact),
                    verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.small),
                ) {
                    Text(
                        text = stringResource(R.string.books),
                        style = MaterialTheme.typography.titleLarge,
                        modifier = Modifier.semantics { heading() },
                    )
                    Text(
                        text = stringResource(R.string.sample_catalogue),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
            if (books.isEmpty()) {
                item {
                    VeritalexMessage(
                        title = stringResource(R.string.no_sample_books),
                        message = stringResource(R.string.empty_sample_explanation),
                    )
                }
            }
            items(books, key = { it.id }) { book ->
                BookListRow(title = book.title, author = book.author)
            }
        }
    }
}

@VeritalexPreviews
@Composable
private fun BooksScreenPreview() {
    VeritalexTheme {
        Surface(modifier = Modifier.fillMaxSize()) {
            BooksScreen(books = SampleCatalogue.books)
        }
    }
}

@VeritalexLargeTextPreviews
@Composable
private fun LongBookPreview() {
    VeritalexTheme {
        Surface {
            BooksScreen(listOf(Book(1, "A very long sample title that needs several lines to remain fully readable", "An author with a very long name")))
        }
    }
}

@VeritalexThemePreviews
@Composable
private fun EmptyBooksPreview() {
    VeritalexTheme { Surface { BooksScreen(emptyList()) } }
}
