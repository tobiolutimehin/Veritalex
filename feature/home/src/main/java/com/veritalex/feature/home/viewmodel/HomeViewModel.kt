package com.veritalex.feature.home.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.repository.BooksRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.emptyFlow
import kotlinx.coroutines.flow.stateIn
import javax.annotation.concurrent.Immutable
import javax.inject.Inject

@HiltViewModel
class HomeViewModel
@Inject
constructor(
    booksRepository: BooksRepository,
) : ViewModel() {
    private val currentSelectedTopic: MutableStateFlow<String?> = MutableStateFlow(null)
    private val currentBookInProgress: MutableStateFlow<Book?> = MutableStateFlow(null)

    private val fetchSavedBooks: Flow<List<Book>> =
        emptyFlow<List<Book>>().stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList(),
        )

    private val recommendedBooks: Flow<List<Book>> =
        booksRepository
            .fetchRecommendedBooks()

    fun selectRecommendedTopic(topic: String) {
        currentSelectedTopic.value = topic
    }

    fun saveBook(book: Book) {}

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
