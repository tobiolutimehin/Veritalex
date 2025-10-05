package com.veritalex.feature.home.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import com.veritalex.feature.home.R

@Composable
fun BookRowItem(
    book: Book,
    modifier: Modifier = Modifier,
    onClick: () -> Unit = {},
) {
    val authorName = book.authors.firstOrNull()?.name
    val unknownAuthorString = stringResource(R.string.unknown_author)
    val fullContentDescription = stringResource(
        R.string.book_cover_content_description,
        book.title,
        authorName ?: unknownAuthorString,
    )

    Column(
        modifier = modifier
            .width(110.dp)
            .clickable(onClick = onClick)
            .semantics(mergeDescendants = true) {
                contentDescription = fullContentDescription
            },
    ) {
        BookCover(book, modifier = Modifier.fillMaxWidth())
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = book.title,
            style = MaterialTheme.typography.titleSmall,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
        )
        Text(
            // Use the memoized variable. Provide a non-breaking space if empty for layout stability.
            text = authorName ?: " ",
            style = MaterialTheme.typography.bodySmall,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
        )
    }
}

@Composable
fun BookCover(
    book: Book,
    modifier: Modifier = Modifier,
) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(book.formats["image/jpeg"])
            .crossfade(true)
            .build(),
        alignment = Alignment.Center,
        modifier = modifier
            .aspectRatio(0.7f)
            .clip(MaterialTheme.shapes.small),
        contentDescription = null,
    )
}

@Preview
@Composable
fun BookCoverPreview() {
    val book = Book(
        id = 1,
        title = "The Great Gatsby",
        subjects = listOf("Fiction"),
        authors = listOf(Person(name = "F. Scott Fitzgerald", birthYear = 1896, deathYear = 1940)),
        translators = emptyList(),
        bookshelves = listOf("Classic Literature"),
        languages = listOf("en"),
        copyright = false,
        mediaType = "Text",
        formats = mapOf(
            "image/jpeg" to "https://www.gutenberg.org/cache/epub/64317/pg64317.cover.medium.jpg",
        ),
        downloadCount = 1000,
    )
    BookCover(book)
}

@Preview
@Composable
fun BookRowItemPreview() {
    val book = Book(
        id = 1,
        title = "The Great Gatsby",
        subjects = listOf("Fiction"),
        authors = listOf(Person(name = "F. Scott Fitzgerald", birthYear = 1896, deathYear = 1940)),
        translators = emptyList(),
        bookshelves = listOf("Classic Literature"),
        languages = listOf("en"),
        copyright = false,
        mediaType = "Text",
        formats = mapOf(
            "image/jpeg" to "https://www.gutenberg.org/cache/epub/64317/pg64317.cover.medium.jpg",
        ),
        downloadCount = 1000,
    )
    MaterialTheme {
        BookRowItem(book = book)
    }
}

