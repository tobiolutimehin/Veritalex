package com.veritalex.feature.home.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.paging.PagingData
import androidx.paging.compose.collectAsLazyPagingItems
import androidx.paging.compose.itemContentType
import androidx.paging.compose.itemKey
import com.veritalex.core.data.models.Book
import kotlinx.coroutines.flow.Flow

@Composable
fun BooksLazyRow(
    books: List<Book>,
    modifier: Modifier = Modifier,
) {
    LazyRow(
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        modifier = modifier,
        contentPadding = PaddingValues(horizontal = 16.dp),
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
    items.let {
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            modifier = modifier,
            contentPadding = PaddingValues(horizontal = 16.dp),
        ) {
            items(
                it.itemCount,
                key = it.itemKey { it.id },
                contentType = it.itemContentType { "contentType" },
            ) { index ->
                val book = items[index]
                book?.let {
                    BookRowItem(book = book)
                }
            }
        }
    }
}
