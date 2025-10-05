package com.veritalex.feature.home.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.paging.PagingData
import androidx.paging.compose.collectAsLazyPagingItems
import androidx.paging.compose.itemContentType
import androidx.paging.compose.itemKey
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import com.veritalex.feature.home.BookRowItem
import com.veritalex.feature.home.ContinueReadingSection
import com.veritalex.feature.home.MyBooksSection
import com.veritalex.feature.home.RecommendedBooksSection
import com.veritalex.feature.home.viewmodel.HomeViewModel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.launch

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

@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel = hiltViewModel(),
) {
    val books = viewModel.books
    val pagerState = rememberPagerState(pageCount = { tabsList.size })
    val coroutineScope = rememberCoroutineScope()
    val selectedTabIndex = remember { derivedStateOf { pagerState.currentPage } }

    Column(modifier = modifier) {
        TabRow(
            selectedTabIndex = selectedTabIndex.value,
            modifier =
                Modifier
                    .fillMaxWidth()
                    .wrapContentHeight(),
        ) {
            tabsList.forEachIndexed { index, tabItem ->
                Tab(
                    selected = index == selectedTabIndex.value,
                    onClick = {
                        coroutineScope.launch {
                            pagerState.animateScrollToPage(index)
                        }
                    },
                    text = { Text(text = tabItem.title) },
                )
            }
        }

        HorizontalPager(
            state = pagerState,
            userScrollEnabled = false,
        ) {
            when (it) {
                0 -> {
                    HomeTab(modifier = Modifier.weight(1f), allBooks = books)
                }

                1 -> {
                    Column { }
                }
            }
        }
    }
}

val tabsList =
    listOf(
        TabItem(
            "Home",
        ),
        TabItem(
            "My saved books",
        ),
    )

data class TabItem(
    val title: String,
    val icon: ImageVector? = null,
)

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
