package com.veritalex.feature.home.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.paging.PagingData
import androidx.paging.compose.collectAsLazyPagingItems
import androidx.paging.compose.itemContentType
import androidx.paging.compose.itemKey
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf

@Composable
fun BooksLazyRow(
    books: List<Book>,
    modifier: Modifier = Modifier,
) {
    LazyRow(
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        modifier = modifier,
    ) {
        items(books) { book ->
            BookRowItem(book = book)
        }
    }
}

@Composable
fun BooksLazyRowPaging(
    books: Flow<PagingData<Book>>,
    modifier: Modifier = Modifier,
) {
    val items = books.collectAsLazyPagingItems()
    items.let { item ->
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            modifier = modifier,
        ) {
            items(
                item.itemCount,
                key = item.itemKey { key -> key.id },
                contentType = item.itemContentType { "contentType" },
            ) { index ->
                val book = items[index]
                book?.let {
                    BookRowItem(book = book)
                }
            }
        }
    }
}

@Preview
@Composable
fun BooksLazyRowPreview() {
    val books = listOf(
        Book(
            id = 1,
            title = "Book Title 1",
            subjects = listOf("Fiction"),
            authors = listOf(Person(name = "Author 1", birthYear = 1900, deathYear = 1980)),
            translators = emptyList(),
            bookshelves = listOf("Bestsellers"),
            languages = listOf("en"),
            copyright = true,
            mediaType = "text/plain",
            formats = emptyMap(),
            downloadCount = 100,
        ),
        Book(
            id = 2,
            title = "Book Title 2",
            subjects = listOf("Science"),
            authors = listOf(Person(name = "Author 2", birthYear = 1920, deathYear = 2000)),
            translators = emptyList(),
            bookshelves = listOf("New Releases"),
            languages = listOf("en"),
            copyright = false,
            mediaType = "text/plain",
            formats = emptyMap(),
            downloadCount = 200,
        ),
    )
    BooksLazyRow(books = books)
}

@Preview
@Composable
fun BooksLazyRowPagingPreview() {
    val books = flowOf(
        PagingData.from(
            listOf(
                Book(
                    id = 1,
                    title = "Book Title 1",
                    subjects = listOf("Fiction"),
                    authors = listOf(Person(name = "Author 1", birthYear = 1900, deathYear = 1980)),
                    translators = emptyList(),
                    bookshelves = listOf("Bestsellers"),
                    languages = listOf("en"),
                    copyright = true,
                    mediaType = "text/plain",
                    formats = emptyMap(),
                    downloadCount = 100,
                ),
                Book(
                    id = 2,
                    title = "Book Title 2",
                    subjects = listOf("Science"),
                    authors = listOf(Person(name = "Author 2", birthYear = 1920, deathYear = 2000)),
                    translators = emptyList(),
                    bookshelves = listOf("New Releases"),
                    languages = listOf("en"),
                    copyright = false,
                    mediaType = "text/plain",
                    formats = emptyMap(),
                    downloadCount = 200,
                ),
            ),
        ),
    )
    BooksLazyRowPaging(books = books)
}
