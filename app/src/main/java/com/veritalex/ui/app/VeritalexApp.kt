package com.veritalex.ui.app

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.windowsizeclass.WindowSizeClass
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import com.veritalex.ui.navigation.VeritalexAppState
import com.veritalex.ui.navigation.rememberVeritalexAppState

@Composable
fun VeritalexApp(
    windowSizeClass: WindowSizeClass,
    veritalexAppState: VeritalexAppState = rememberVeritalexAppState(
        windowSizeClass = windowSizeClass,
    ),
    ){

    val snackbarHostState = remember { SnackbarHostState() }
    
    Scaffold(
        topBar = {},
        modifier = Modifier.fillMaxSize(),
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { paddingValues ->  
        paddingValues
    }
    }