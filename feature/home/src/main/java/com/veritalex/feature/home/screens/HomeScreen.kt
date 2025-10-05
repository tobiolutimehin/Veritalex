package com.veritalex.feature.home.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.paging.PagingData
import androidx.paging.compose.collectAsLazyPagingItems
import androidx.paging.compose.itemContentType
import androidx.paging.compose.itemKey
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.veritalex.core.data.models.Book
import com.veritalex.feature.home.viewmodel.HomeViewModel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.launch

@Composable
fun BooksLazyRow(
    books: Flow<PagingData<Book>>,
    modifier: Modifier = Modifier,
) {
    val items = books.collectAsLazyPagingItems()
    items.let {
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            modifier = modifier,
        ) {
            items(
                it.itemCount,
                key = it.itemKey { it.id },
                contentType = it.itemContentType { "contentType" },
            ) { index ->
                val book = items[index]
                book?.let {
                    BookCover(book = book)
                }
            }
        }
    }
}

@Composable
fun BookCover(
    book: Book,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier = modifier.width(100.dp),
    ) {
        AsyncImage(
            model =
                ImageRequest
                    .Builder(LocalContext.current)
                    .data(book.formats["image/jpeg"])
                    .crossfade(true)
                    .build(),
            alignment = Alignment.Center,
            modifier =
                Modifier
                    .aspectRatio(0.65f) // 100.dp / 157.dp = 0.64 (approx)
                    .size(100.dp, 0.dp),
            contentDescription = "",
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = book.title,
            style = MaterialTheme.typography.bodyMedium,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
        )
        Text(
            text = book.authors.getOrNull(0)?.name ?: "",
            style = MaterialTheme.typography.bodySmall,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
        )
        Text(text = book.downloadCount.toString())
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

        HorizontalPager(state = pagerState) {
            when (it) {
                0 -> {
                    HomeTab(modifier = Modifier.weight(1f), allBooks = books)
                }

                1 -> {
                    BookSection(modifier = Modifier.weight(1f))
                }
            }
        }
    }
}

val tabsList =
    listOf(
        TabItem(
            "Home",
            {
//        Text(text = "Home")
            },
        ),
        TabItem(
            "My saved books",
            {
//        Text(text = "My saved books")
            },
        ),
    )

data class TabItem(
    val title: String,
    val screen: @Composable () -> Unit,
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
        val book: Book? = null
        book?.let {
            ContinueReadingSection(book = it)
        }
        allBooks?.let {
            BooksLazyRow(books = it)
        }
    }
}

@Composable
fun BookSection(modifier: Modifier) {
}

@Composable
fun ContinueReadingSection(
    book: Book,
    modifier: Modifier = Modifier,
    onClick: () -> Unit = {},
) {
    Column(
        modifier =
            modifier
                .fillMaxWidth()
                .wrapContentHeight(),
    ) {
        Text(text = "Continue Reading")
        Row {
            BookCover(book = book)
            Column {
                Text(text = book.title)
                Text(text = book.authors.toString())
                Spacer(modifier = Modifier.weight(1f))
                Button(onClick = onClick) {
                    Text(text = "Continue Reading")
                }
            }
        }
    }
}
