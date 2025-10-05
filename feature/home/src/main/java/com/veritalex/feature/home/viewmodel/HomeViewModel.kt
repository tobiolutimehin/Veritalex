package com.veritalex.feature.home.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.paging.PagingData
import androidx.paging.cachedIn
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.repository.BooksRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.annotation.concurrent.Immutable
import javax.inject.Inject

@HiltViewModel
class HomeViewModel
    @Inject
    constructor(
        private val booksRepository: BooksRepository,
    ) : ViewModel() {
        private val currentSelectedTopic: MutableStateFlow<String?> = MutableStateFlow(null)
        private val currentBookInProgress: MutableStateFlow<Book?> = MutableStateFlow(null)

        private val fetchSavedBooks: StateFlow<List<Book>> =
            booksRepository.fetchSavedBooks().stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5000),
                initialValue = emptyList(),
            )

        private val recommendedBooks: Flow<List<Book>> =
            booksRepository.fetchRecommendedBooks().stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5000),
                initialValue = emptyList(),
        )

    val books: Flow<PagingData<Book>> =
        booksRepository
            .fetchBooks()
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5000),
                initialValue = PagingData.empty(),
            ).cachedIn(viewModelScope)

    fun selectRecommendedTopic(topic: String) {
        currentSelectedTopic.value = topic
    }

    fun saveBook(book: Book) {
        viewModelScope.launch {
            booksRepository.saveBook(book.id.toString())
        }
    }

    val uiState: StateFlow<HomeUiState> =
        combine(
            fetchSavedBooks,
            recommendedBooks,
            currentBookInProgress,
        ) { savedBooks, recommendedBooks, currentBookInProgress ->
            try {
                HomeUiState.Success(
                    savedBooks = savedBooks,
                    recommendedBooks = recommendedBooks,
                    inProgressBook = currentBookInProgress,
                )
            } catch (e: Exception) {
                HomeUiState.Error(e.message)
            }
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = HomeUiState.Loading,
        )
}

@Immutable
sealed interface HomeUiState {
    data object Loading : HomeUiState

    data class Success(
        val inProgressBook: Book? = null,
        val recommendedBooks: List<Book> = emptyList(),
        val savedBooks: List<Book> = emptyList(),
    ) : HomeUiState

    data class Error(
        val errorMessage: String? = null,
    ) : HomeUiState
}
