package com.veritalex.feature.home.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.hilt.navigation.compose.hiltViewModel
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import com.veritalex.feature.home.navigation.TabItem.Companion.tabsList
import com.veritalex.feature.home.ui.BooksLazyColumn
import com.veritalex.feature.home.ui.HomeTab
import com.veritalex.feature.home.viewmodel.HomeViewModel
import kotlinx.coroutines.launch

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
                    text = { Text(text = stringResource(tabItem.title)) },
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
                    val books = listOf(
                        Book(
                            id = 1,
                            title = "Book Title 1",
                            subjects = listOf("Fiction"),
                            authors = listOf(
                                Person(
                                    name = "Author 1",
                                    birthYear = 1900,
                                    deathYear = 1980,
                                ),
                            ),
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
                            authors = listOf(
                                Person(
                                    name = "Author 2",
                                    birthYear = 1920,
                                    deathYear = 2000,
                                ),
                            ),
                            translators = emptyList(),
                            bookshelves = listOf("New Releases"),
                            languages = listOf("en"),
                            copyright = false,
                            mediaType = "text/plain",
                            formats = emptyMap(),
                            downloadCount = 200,
                        ),
                    )
                    SavedBooksTab(savedBooks = books, modifier = Modifier.weight(1f))
                }
            }
        }
    }
}

@Composable
fun SavedBooksTab(
    savedBooks: List<Book>,
    modifier: Modifier = Modifier,
) {
    BooksLazyColumn(savedBooks = savedBooks, modifier = modifier)
}