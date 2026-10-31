package com.veritalex.feature.home.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.semantics.clearAndSetSemantics
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
import coil3.compose.AsyncImage
import coil3.request.ImageRequest
import coil3.request.crossfade
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import com.veritalex.feature.home.R

@Composable
fun BookRowItem(
    book: Book,
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null,
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
            .then(if (onClick == null) Modifier else Modifier.clickable(onClick = onClick))
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
    Box(
        modifier = modifier.aspectRatio(2f / 3f)
            .clip(MaterialTheme.shapes.extraSmall)
            .background(MaterialTheme.colorScheme.secondaryContainer)
            .clearAndSetSemantics { },
    ) {
        Column(
            modifier = Modifier.fillMaxSize().padding(8.dp),
            verticalArrangement = Arrangement.SpaceBetween,
        ) {
            Text(
                book.title, style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.onSecondaryContainer,
                maxLines = 4, overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f),
            )
            Text(
                book.authors.firstOrNull()?.name ?: stringResource(R.string.unknown_author),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSecondaryContainer,
                maxLines = 2, overflow = TextOverflow.Ellipsis,
            )
        }
        AsyncImage(
            model = ImageRequest.Builder(LocalContext.current)
                .data(book.formats["image/jpeg"]).crossfade(true).build(),
            modifier = Modifier.fillMaxSize(),
            contentScale = ContentScale.Crop,
            contentDescription = null,
        )
    }
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
    com.veritalex.core.designsystem.theme.VeritalexTheme {
        BookRowItem(book = book)
    }
}

