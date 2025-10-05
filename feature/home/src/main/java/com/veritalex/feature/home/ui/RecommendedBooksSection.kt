package com.veritalex.feature.home.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.paging.PagingData
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import com.veritalex.feature.home.R
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf

@Composable
fun RecommendedBooksSection(
    books: Flow<PagingData<Book>>,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier =
            modifier
                .fillMaxWidth()
                .wrapContentHeight()
                .padding(vertical = 24.dp, horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        val continueReading = stringResource(R.string.recommended_books)
        Text(text = continueReading, style = MaterialTheme.typography.headlineSmall)
        BooksLazyRowPaging(books = books)
    }
}

@Preview
@Composable
fun RecommendedBooksSectionPreview() {
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
    val books = flowOf(PagingData.from(listOf(book, book, book, book)))
    RecommendedBooksSection(
        books = books,
    )
}
