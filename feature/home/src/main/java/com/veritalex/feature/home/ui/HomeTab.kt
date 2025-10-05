package com.veritalex.feature.home.ui

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.HorizontalDivider
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.paging.PagingData
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf

@Composable
fun HomeTab(
    modifier: Modifier = Modifier,
    allBooks: Flow<PagingData<Book>>? = null,
) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(vertical = 16.dp),
    ) {
        val book =
            Book(
                id = 1,
                title = "Pride and Prejudice",
                subjects = listOf("Love stories", "Sisters Fiction"),
                authors =
                    listOf(
                        Person(
                            birthYear = 1775,
                            deathYear = 1817,
                            name = "Austen, Jane",
                        ),
                    ),
                translators = emptyList(),
                bookshelves = listOf("Best Books Ever Listings", "Harvard Classics"),
                languages = listOf("en"),
                copyright = false,
                mediaType = "Text",
                formats = mapOf("image/jpeg" to "https://www.gutenberg.org/cache/epub/1342/pg1342.cover.small.jpg"),
                downloadCount = 50000,
            )
        item { ContinueReadingSection(book = book) }
        item {
            HorizontalDivider()
        }
        item { MyBooksSection(listOf(book, book, book, book, book)) }
        item {
            HorizontalDivider()
        }
        item {
            allBooks?.let {
                RecommendedBooksSection(allBooks)
            }
        }
    }
}

@Preview
@Composable
fun HomeTabPreview() {
    val books =
        listOf(
            Book(
                id = 1,
                title = "Pride and Prejudice",
                subjects = listOf("Love stories", "Sisters Fiction"),
                authors =
                    listOf(
                        Person(
                            birthYear = 1775,
                            deathYear = 1817,
                            name = "Austen, Jane",
                        ),
                    ),
                translators = emptyList(),
                bookshelves = listOf("Best Books Ever Listings", "Harvard Classics"),
                languages = listOf("en"),
                copyright = false,
                mediaType = "Text",
                formats =
                    mapOf(
                        "image/jpeg" to
                                "https://www.gutenberg.org/cache/epub/1342/pg1342.cover.small.jpg",
                    ),
                downloadCount = 50000,
            ),
        )
    val pagingData = PagingData.from(books)
    val allBooks = flowOf(pagingData)
    HomeTab(
        allBooks = allBooks,
    )
}

