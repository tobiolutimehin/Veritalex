package com.veritalex.feature.home.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.paging.PagingData
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import kotlinx.coroutines.flow.Flow

@Composable
fun HomeTab(
    modifier: Modifier = Modifier,
    allBooks: Flow<PagingData<Book>>? = null,
) {
    Column(
        modifier = modifier.verticalScroll(rememberScrollState()),
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
        ContinueReadingSection(book = book)
        MyBooksSection(listOf(book, book, book, book, book))
        allBooks?.let {
            RecommendedBooksSection(allBooks)
        }
    }
}
