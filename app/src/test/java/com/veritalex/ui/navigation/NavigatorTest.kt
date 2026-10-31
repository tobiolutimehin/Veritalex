package com.veritalex.ui.navigation

import androidx.compose.runtime.mutableStateOf
import androidx.navigation3.runtime.NavBackStack
import androidx.navigation3.runtime.NavKey
import com.veritalex.core.navigation.HomeRoute
import com.veritalex.core.navigation.LibraryRoute
import com.veritalex.core.navigation.SettingsRoute
import org.junit.Assert.assertEquals
import org.junit.Test

class NavigatorTest {
    private fun navigator(): Navigator = Navigator(
        NavigationState(
            startRoute = HomeRoute,
            topLevelRoute = mutableStateOf<NavKey>(HomeRoute),
            backStacks = mapOf(
                HomeRoute to NavBackStack<NavKey>(HomeRoute),
                LibraryRoute to NavBackStack<NavKey>(LibraryRoute),
            ),
        ),
    )

    @Test
    fun openingTheSameDetailTwiceAddsOnlyOneEntry() {
        val navigator = navigator()
        navigator.navigate(SettingsRoute)
        navigator.navigate(SettingsRoute)
        assertEquals(listOf(HomeRoute, SettingsRoute), navigator.state.backStacks[HomeRoute])
    }

    @Test
    fun backFromDetailKeepsItsInvokingDestination() {
        val navigator = navigator()
        navigator.navigate(LibraryRoute)
        navigator.navigate(SettingsRoute)
        navigator.goBack()
        assertEquals(LibraryRoute, navigator.state.topLevelRoute)
        assertEquals(listOf(LibraryRoute), navigator.state.backStacks[LibraryRoute])
    }

    @Test
    fun switchingDestinationsPreservesTheirStacks() {
        val navigator = navigator()
        navigator.navigate(LibraryRoute)
        navigator.navigate(SettingsRoute)
        navigator.navigate(HomeRoute)
        navigator.navigate(LibraryRoute)
        assertEquals(listOf(LibraryRoute, SettingsRoute), navigator.state.backStacks[LibraryRoute])
    }

    @Test
    fun backAtDestinationRootReturnsHomeWithoutRemovingRoots() {
        val navigator = navigator()
        navigator.navigate(LibraryRoute)
        navigator.goBack()
        navigator.goBack()
        assertEquals(HomeRoute, navigator.state.topLevelRoute)
        assertEquals(listOf(HomeRoute), navigator.state.backStacks[HomeRoute])
        assertEquals(listOf(LibraryRoute), navigator.state.backStacks[LibraryRoute])
    }
}
