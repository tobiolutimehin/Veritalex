package com.veritalex.feature.home.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.paging.cachedIn
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.repository.BooksRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@OptIn(ExperimentalCoroutinesApi::class)
@HiltViewModel
class HomeViewModel @Inject constructor(private val booksRepository: BooksRepository) : ViewModel() {
    private val refresh = MutableStateFlow(0)
    val books = booksRepository.fetchBooks().cachedIn(viewModelScope)

    val uiState: StateFlow<HomeUiState> = refresh.flatMapLatest {
        booksRepository.fetchSavedBooks()
            .map<List<Book>, HomeUiState> { HomeUiState.Success(it) }
            .onStart { emit(HomeUiState.Loading) }
            .catch { emit(HomeUiState.Error) }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), HomeUiState.Loading)

    fun retry() { refresh.update { it + 1 } }

    fun saveBook(book: Book) {
        viewModelScope.launch { booksRepository.saveBook(book.id.toString()) }
    }
}

sealed interface HomeUiState {
    data object Loading : HomeUiState
    data class Success(val savedBooks: List<Book>) : HomeUiState
    data object Error : HomeUiState
}
