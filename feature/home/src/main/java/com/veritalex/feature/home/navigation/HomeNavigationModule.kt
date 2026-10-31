package com.veritalex.feature.home.navigation

import com.veritalex.feature.home.screens.HomeScreen
import com.veritalex.feature.home.screens.ExploreScreen
import com.veritalex.feature.home.screens.LibraryScreen
import com.veritalex.core.navigation.ExploreRoute
import com.veritalex.core.navigation.LibraryRoute
import com.veritalex.core.navigation.EntryProviderInstaller
import com.veritalex.core.navigation.HomeRoute
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.components.ActivityRetainedComponent
import dagger.multibindings.IntoSet

@Module
@InstallIn(ActivityRetainedComponent::class)
object HomeNavigationModule {
    @IntoSet
    @Provides
    fun provideEntryProviderInstaller(): EntryProviderInstaller = {
        entry<HomeRoute> { HomeScreen() }
        entry<ExploreRoute> { ExploreScreen() }
        entry<LibraryRoute> { LibraryScreen() }
    }
}
