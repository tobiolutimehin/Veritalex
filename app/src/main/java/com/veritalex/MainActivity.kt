package com.veritalex

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.consumeWindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import com.veritalex.core.designsystem.theme.VeritalexTheme
import com.veritalex.feature.books.BooksScreen
import com.veritalex.feature.books.SampleCatalogue

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            VeritalexTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { padding ->
                    BooksScreen(
                        books = SampleCatalogue.books,
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(padding)
                            .consumeWindowInsets(padding),
                    )
                }
            }
        }
    }
}
