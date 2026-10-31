package com.veritalex.feature.home

import androidx.paging.PagingData
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.repository.BooksRepository
import com.veritalex.feature.home.viewmodel.HomeUiState
import com.veritalex.feature.home.viewmodel.HomeViewModel
import java.io.IOException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runCurrent
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.junit.Assert.assertEquals
import org.junit.Test
import org.junit.Before
import org.junit.After
import kotlinx.coroutines.test.StandardTestDispatcher

@OptIn(ExperimentalCoroutinesApi::class)
class HomeViewModelTest {
    @Before
    fun setUp() { Dispatchers.setMain(StandardTestDispatcher()) }

    @After
    fun tearDown() { Dispatchers.resetMain() }

    @Test
    fun failedSavedBooksLoadCanBeRetried() = runTest {

        var offline = true
        val repository = object : BooksRepository {
            override fun fetchBooks() = flowOf(PagingData.empty<Book>())
            override fun fetchRecommendedBooks(topic: String?) = flowOf(emptyList<Book>())
            override suspend fun saveBook(id: String) = Unit
            override fun fetchSavedBooks() = flow {
                if (offline) throw IOException("Offline")
                emit(emptyList<Book>())
            }
        }
        val viewModel = HomeViewModel(repository)
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) { viewModel.uiState.collect {} }
        runCurrent()
        assertEquals(HomeUiState.Error, viewModel.uiState.value)
        offline = false
        viewModel.retry()
        runCurrent()
        assertEquals(HomeUiState.Success(emptyList()), viewModel.uiState.value)
    }
}
