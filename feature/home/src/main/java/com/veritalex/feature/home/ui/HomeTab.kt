package com.veritalex.feature.home.ui

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.paging.PagingData
import com.veritalex.core.data.models.Book
import com.veritalex.core.designsystem.theme.VeritalexTheme
import kotlinx.coroutines.flow.Flow

@Composable
fun HomeTab(
    modifier: Modifier = Modifier,
    allBooks: Flow<PagingData<Book>>? = null,
    myBooks: List<Book> = emptyList(),
) {
    LazyColumn(modifier = modifier, contentPadding = PaddingValues(vertical = 16.dp)) {
        if (myBooks.isNotEmpty()) item { MyBooksSection(myBooks) }
        item { allBooks?.let { RecommendedBooksSection(it) } }
    }
}

@Preview(showBackground = true)
@Preview(showBackground = true, uiMode = android.content.res.Configuration.UI_MODE_NIGHT_YES)
@Composable
private fun HomeTabPreview() {
    VeritalexTheme {
        HomeTab(allBooks = kotlinx.coroutines.flow.flowOf(PagingData.empty()))
    }
}
