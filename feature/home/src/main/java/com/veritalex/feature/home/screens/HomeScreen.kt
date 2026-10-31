package com.veritalex.feature.home.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.lifecycle.viewmodel.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.veritalex.feature.home.R
import com.veritalex.feature.home.ui.BooksLazyColumn
import com.veritalex.feature.home.ui.HomeTab
import com.veritalex.feature.home.ui.RecommendedBooksSection
import com.veritalex.feature.home.viewmodel.HomeUiState
import com.veritalex.feature.home.viewmodel.HomeViewModel

@Composable
fun HomeScreen(modifier: Modifier = Modifier, viewModel: HomeViewModel = hiltViewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    when (val current = state) {
        is HomeUiState.Success -> HomeTab(modifier, viewModel.books, current.savedBooks)
        else -> BookLoadState(state, viewModel::retry, modifier)
    }
}

@Composable
fun ExploreScreen(modifier: Modifier = Modifier, viewModel: HomeViewModel = hiltViewModel()) {
    Column(modifier.fillMaxSize()) { RecommendedBooksSection(viewModel.books) }
}

@Composable
fun LibraryScreen(modifier: Modifier = Modifier, viewModel: HomeViewModel = hiltViewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    when (val current = state) {
        is HomeUiState.Success -> if (current.savedBooks.isEmpty()) {
            Box(modifier.fillMaxSize().padding(20.dp), contentAlignment = Alignment.Center) {
                Text(stringResource(R.string.no_saved_books))
            }
        } else BooksLazyColumn(current.savedBooks, modifier)
        else -> BookLoadState(state, viewModel::retry, modifier)
    }
}

@Composable
private fun BookLoadState(state: HomeUiState, onRetry: () -> Unit, modifier: Modifier) {
    Box(modifier.fillMaxSize().padding(20.dp), contentAlignment = Alignment.Center) {
        if (state is HomeUiState.Loading) CircularProgressIndicator() else Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text(stringResource(R.string.books_load_error))
            TextButton(onClick = onRetry) { Text(stringResource(R.string.retry)) }
        }
    }
}
