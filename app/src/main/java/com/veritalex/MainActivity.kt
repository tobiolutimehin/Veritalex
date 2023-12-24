package com.veritalex

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.material3.adaptive.ExperimentalMaterial3AdaptiveApi
import androidx.compose.material3.adaptive.currentWindowAdaptiveInfo
import androidx.compose.material3.adaptive.navigation.suite.ExperimentalMaterial3AdaptiveNavigationSuiteApi
import androidx.compose.material3.adaptive.navigation.suite.NavigationSuiteScaffold
import androidx.compose.material3.adaptive.navigation.suite.NavigationSuiteScaffoldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.paging.PagingData
import androidx.paging.compose.collectAsLazyPagingItems
import androidx.paging.compose.itemContentType
import androidx.paging.compose.itemKey
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.repository.BooksRepository
import com.veritalex.core.designsystem.theme.VeritalexTheme
import dagger.hilt.android.AndroidEntryPoint
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val viewModel: SampleViewModel = viewModel()
            val items = viewModel.uiState.books?.collectAsLazyPagingItems()
            VeritalexTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background,
                ) {
                    items?.let{
                        LazyRow(
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            items(
                                it.itemCount,
                                key = it.itemKey { it.id },
                                contentType = it.itemContentType { "contentType" },
                            ) {
                                val item = items[it]
                                if (item != null) {
                                    BookCover(book = item)
                                }
                            }
                        }
                    }
                }
//                    HomeScreen()
//                VeritalexApp()
            }
        }
    }
}

@Composable
fun BookCover(
    book: Book,
    modifier: Modifier = Modifier
) {
    Column (
        modifier = modifier.width(100.dp)
    ){
        AsyncImage(
            model =
            ImageRequest
                .Builder(LocalContext.current)
                .data(book.formats["image/jpeg"])
                .crossfade(true)
                .build(),
            alignment = Alignment.Center,
            modifier = Modifier
                .aspectRatio(0.65f) // 100.dp / 157.dp = 0.64 (approx)
                .size(100.dp, 0.dp),
            contentDescription = "",
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(text = book.title, style = MaterialTheme.typography.bodyMedium, maxLines = 1, overflow = TextOverflow.Ellipsis)
        Text(text = book.authors.getOrNull(0)?.name ?: "", style = MaterialTheme.typography.bodySmall, maxLines = 1, overflow = TextOverflow.Ellipsis)
        Text(text = book.downloadCount.toString())
    }
}

@Composable
fun BooksLazyRow(
    books: Flow<PagingData<Book>>,
    modifier: Modifier = Modifier
) {
    val items = books.collectAsLazyPagingItems()
    items.let{
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            modifier = modifier
        ) {
            items(
                it.itemCount,
                key = it.itemKey { it.id },
                contentType = it.itemContentType { "contentType" },
            ) {index ->
                val book = items[index]
                book?.let {
                    BookCover(book = book)
                }
            }
        }
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun HomeScreen(
    modifier: Modifier = Modifier
) {
    val pagerState = rememberPagerState(pageCount = { tabs.size })
    val coroutineScope = rememberCoroutineScope()

    Column(modifier = modifier) {
        TabRow(
            selectedTabIndex = pagerState.currentPage,
            modifier = Modifier
                .fillMaxWidth()
                .wrapContentHeight()
        ) {
            tabs.forEachIndexed { index, tabItem ->
                Tab(
                    selected = index == pagerState.currentPage,
                    onClick = {
                        coroutineScope.launch {
                            pagerState.scrollToPage(index)
                        }
                    },
                    text = { Text(text = tabItem.title) },

                    )
            }
        }

        HorizontalPager(state = pagerState) {
            Row{ Text(tabs[pagerState.currentPage].title) }
        }
    }
}
val tabs = listOf(
    TabItem("Home", {
        Text(text = "Home")
    }),
    TabItem("My saved books", {
        Text(text = "My saved books")
    })
)
data class TabItem (
    val title: String,
    val screen: @Composable () -> Unit,
    val icon: ImageVector? = null,
)

@Composable
fun ContinueReadingSection(
    book: Book,
    modifier: Modifier = Modifier,
    onClick: () -> Unit = {}
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .wrapContentHeight()
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

@HiltViewModel
class SampleViewModel @Inject constructor(
    private val booksRepository: BooksRepository,
) : ViewModel() {
    var uiState: BooksUi by mutableStateOf(BooksUi())
    fun getBooks() {
        viewModelScope.launch {
            uiState = BooksUi(booksRepository.fetchBooks())
        }
    }

    init {
        getBooks()
    }
}

data class BooksUi(
    val books: Flow<PagingData<Book>>? = null
)

@OptIn(ExperimentalMaterial3AdaptiveNavigationSuiteApi::class,
    ExperimentalMaterial3AdaptiveApi::class
)
@Composable
fun VeritalexApp() {

    val navSuiteType =
        NavigationSuiteScaffoldDefaults.calculateFromAdaptiveInfo(currentWindowAdaptiveInfo())


    NavigationSuiteScaffold(
        navigationSuiteItems = { -> },
        modifier = Modifier,
    ) {

    }
}
