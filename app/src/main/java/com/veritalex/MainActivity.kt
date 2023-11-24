package com.veritalex

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import com.veritalex.core.data.repository.BooksRepository
import com.veritalex.ui.theme.VeritalexTheme
import dagger.hilt.android.AndroidEntryPoint
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val viewModel: SampleViewModel = viewModel()
            VeritalexTheme {
                viewModel.getBooks()
                VeritalexApp()
            }
        }
    }
}

@Composable
fun VeritalexApp() {
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background,
    ) {
        Text(text = "Hello World!")
    }
}

@HiltViewModel
class SampleViewModel @Inject constructor(
    private val booksRepository: BooksRepository,
) : ViewModel() {

    fun getBooks() {
        viewModelScope.launch {
            Log.d("tobistuff", booksRepository.fetchBooks().toString())
        }
    }
}
