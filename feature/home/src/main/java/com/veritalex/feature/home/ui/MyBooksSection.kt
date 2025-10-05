package com.veritalex.feature.home.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import com.veritalex.feature.home.R

@Composable
fun MyBooksSection(
    myBooks: List<Book>,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier =
            modifier
                .fillMaxWidth()
                .wrapContentHeight()
                .padding(vertical = 24.dp, horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        val continueReading = stringResource(R.string.saved_books)
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(text = continueReading, style = MaterialTheme.typography.headlineSmall)

            TextButton(
                onClick = { },
                contentPadding = ButtonDefaults.TextButtonWithIconContentPadding,
            ) {
                Text(stringResource(R.string.see_all))
                Spacer(Modifier.size(ButtonDefaults.IconSpacing))
                Icon(
                    imageVector = Icons.Default.Home,
                    contentDescription = null,
                    modifier = Modifier.size(ButtonDefaults.IconSize),
                )
            }

        }
        BooksLazyRow(books = myBooks)
    }
}


@Preview
@Composable
fun MyBooksSectionPreview() {
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
    val myBooks = listOf(book, book, book)
    MyBooksSection(myBooks = myBooks)
}
