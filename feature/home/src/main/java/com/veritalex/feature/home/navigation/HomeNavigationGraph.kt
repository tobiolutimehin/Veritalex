package com.veritalex.feature.home.navigation

import androidx.navigation.NavGraphBuilder
import androidx.navigation.compose.composable
import com.veritalex.feature.home.screens.HomeScreen

const val HOME_ROUTE = "home"

fun NavGraphBuilder.homeScreen() {
    composable(
        route = HOME_ROUTE,
    ) {
        HomeScreen()
    }
}
