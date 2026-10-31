package com.veritalex.ui.app

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Explore
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.ui.NavDisplay
import com.veritalex.R
import com.veritalex.core.designsystem.icons.VeritalexIcons
import com.veritalex.core.navigation.EntryProviderInstaller
import com.veritalex.core.navigation.ExploreRoute
import com.veritalex.core.navigation.HomeRoute
import com.veritalex.core.navigation.LibraryRoute
import com.veritalex.core.navigation.SettingsRoute
import com.veritalex.ui.navigation.Navigator
import com.veritalex.ui.navigation.rememberNavigationState
import com.veritalex.ui.navigation.toEntries

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VeritalexApp(entryProviderScopes: Set<EntryProviderInstaller>) {
    val state = rememberNavigationState(HomeRoute, setOf(HomeRoute, ExploreRoute, LibraryRoute))
    val navigator = remember(state) { Navigator(state) }
    val route = state.backStacks.getValue(state.topLevelRoute).last()
    val title = stringResource(when (route) {
        ExploreRoute -> R.string.explore
        LibraryRoute -> R.string.library
        SettingsRoute -> R.string.settings
        else -> R.string.app_name
    })
    val provider = entryProvider {
        entryProviderScopes.forEach { installer -> installer() }
        entry<SettingsRoute> {
            Column {
                ListItem(
                    headlineContent = { Text(stringResource(R.string.appearance)) },
                    supportingContent = { Text(stringResource(R.string.appearance_system)) },
                )
            }
        }
    }

    NavigationSuiteScaffold(
        modifier = Modifier.fillMaxSize(),
        navigationSuiteItems = {
            listOf(
                Triple(HomeRoute, R.string.home, VeritalexIcons.Home),
                Triple(ExploreRoute, R.string.explore, Icons.Rounded.Explore),
                Triple(LibraryRoute, R.string.library, VeritalexIcons.Library),
            ).forEach { (destination, label, icon) ->
                item(
                    selected = state.topLevelRoute == destination,
                    onClick = { navigator.navigate(destination) },
                    icon = { Icon(icon, contentDescription = null) },
                    label = { Text(stringResource(label)) },
                )
            }
        },
    ) {
        Scaffold(
            modifier = Modifier.fillMaxSize(),
            topBar = {
                TopAppBar(
                    title = {
                        Column {
                            Text(title, style = MaterialTheme.typography.titleLarge, color = if (route == HomeRoute) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface)
                            if (route == HomeRoute) Text(
                                stringResource(R.string.saved_on_device),
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    },
                    navigationIcon = {
                        if (route == SettingsRoute) IconButton(onClick = navigator::goBack) {
                            Icon(VeritalexIcons.ArrowBack, stringResource(R.string.back))
                        }
                    },
                    actions = {
                        if (route != SettingsRoute) IconButton(onClick = { navigator.navigate(SettingsRoute) }) {
                            Icon(VeritalexIcons.Settings, stringResource(R.string.settings))
                        }
                    },
                )
            },
        ) { padding ->
            NavDisplay(
                entries = state.toEntries(provider),
                modifier = Modifier.padding(padding).fillMaxSize(),
                onBack = navigator::goBack,
            )
        }
    }
}
