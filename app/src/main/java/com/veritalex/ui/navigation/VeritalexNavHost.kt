package com.veritalex.ui.navigation

import androidx.compose.material3.windowsizeclass.WindowSizeClass
import androidx.compose.material3.windowsizeclass.WindowWidthSizeClass
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Stable
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.navigation.NavDestination
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navOptions
import com.veritalex.feature.home.navigation.HOME_ROUTE
import com.veritalex.feature.home.navigation.homeScreen
import kotlinx.coroutines.CoroutineScope

@Composable
fun rememberVeritalexAppState(
    windowSizeClass: WindowSizeClass,
    coroutineScope: CoroutineScope = rememberCoroutineScope(),
    navController: NavHostController = rememberNavController(),
): VeritalexAppState =
    remember(
        navController,
        coroutineScope,
        windowSizeClass,
    ) {
        VeritalexAppState(
            navController,
            coroutineScope,
            windowSizeClass,
        )
    }

@Stable
class VeritalexAppState(
    val navController: NavHostController,
    val coroutineScope: CoroutineScope,
    val windowSizeClass: WindowSizeClass,
) {
    val currentDestination: NavDestination?
        @Composable get() =
            navController
                .currentBackStackEntryAsState()
                .value
                ?.destination

    val currentTopLevelDestination: TopLevelDestination?
        @Composable get() =
            when (currentDestination?.route) {
                else -> null
            }

    val shouldShowBottomBar: Boolean
        get() = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Compact

    val shouldShowNavRail: Boolean
        get() = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Medium

    val shouldShowNavDrawer: Boolean
        get() = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Expanded

    /**
     * Map of top level destinations to be used in the TopBar, BottomBar and NavRail. The key is the
     * route.
     */
    val topLevelDestinations: List<TopLevelDestination> = TopLevelDestination.entries

    /**
     * UI logic for navigating to a top level destination in the app. Top level destinations have
     * only one copy of the destination of the back stack, and save and restore state whenever you
     * navigate to and from it.
     *
     * @param topLevelDestination: The destination the app needs to navigate to.
     */
    fun navigateToTopLevelDestination(topLevelDestination: TopLevelDestination) {
        navOptions {
            // Pop up to the start destination of the graph to
            // avoid building up a large stack of destinations
            // on the back stack as users select items
            popUpTo(navController.graph.findStartDestination().id) {
                saveState = true
            }
            // Avoid multiple copies of the same destination when
            // reselecting the same item
            launchSingleTop = true
            // Restore state when reselecting a previously selected item
            restoreState = true

            when (topLevelDestination) {
                else -> {}
            }
        }
    }

    fun navigateToSearch() {
    }
}

enum class TopLevelDestination {
    Home,
    Library,
    Profile,
    Settings,
}

@Composable
fun VeritalexNavHost(
    appState: VeritalexAppState,
    modifier: Modifier = Modifier,
    startDestination: String = HOME_ROUTE,
) {
    val navController = appState.navController

    NavHost(
        navController = navController,
        startDestination = startDestination,
        modifier = modifier,
    ) {
        homeScreen()
    }
}
