package com.veritalex.core.designsystem.gallery

import android.os.Build
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.consumeWindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import com.veritalex.core.designsystem.theme.AppAppearance
import com.veritalex.core.designsystem.theme.AppColorSource
import com.veritalex.core.designsystem.theme.VeritalexLayout
import com.veritalex.core.designsystem.theme.VeritalexSpacing
import com.veritalex.core.designsystem.theme.VeritalexTheme
import com.veritalex.core.designsystem.preview.VeritalexPreviews
import kotlinx.coroutines.launch

/** All remembered values here are disposable demonstration state, never app settings. */
@Composable
fun DesignSystemGallery(onDarkThemeChanged: (Boolean) -> Unit = {}) {
    var appearance by rememberSaveable { mutableStateOf(AppAppearance.System) }
    var colors by rememberSaveable { mutableStateOf(AppColorSource.Brand) }
    val snackbar = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    VeritalexTheme(appearance, colors) {
        val dark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
        SideEffect { onDarkThemeChanged(dark) }
        Scaffold(snackbarHost = { SnackbarHost(snackbar) }) { insets ->
            GalleryContent(
                appearance, { appearance = it }, colors, { colors = it },
                onShowSnackbar = { scope.launch { snackbar.showSnackbar("Example feedback", withDismissAction = true) } },
                modifier = Modifier.padding(insets).consumeWindowInsets(insets),
            )
        }
    }
}

@Composable
private fun GalleryContent(
    appearance: AppAppearance,
    onAppearance: (AppAppearance) -> Unit,
    colorSource: AppColorSource,
    onColorSource: (AppColorSource) -> Unit,
    onShowSnackbar: () -> Unit,
    modifier: Modifier = Modifier,
) {
    var section by rememberSaveable { mutableStateOf("All") }
    var menu by remember { mutableStateOf(false) }
    LazyVerticalGrid(
        columns = GridCells.Adaptive(320.dp),
        modifier = modifier.fillMaxSize().testTag("gallery"),
        contentPadding = PaddingValues(VeritalexLayout.gutter),
        horizontalArrangement = Arrangement.spacedBy(VeritalexSpacing.extraLarge),
        verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.extraLarge),
    ) {
        item(span = { GridItemSpan(maxLineSpan) }) {
            GallerySection("Veritalex UI gallery") {
                Text("Debug specimens · local demo state only", style = MaterialTheme.typography.bodyMedium)
                FlowRow(horizontalArrangement = Arrangement.spacedBy(VeritalexSpacing.small)) {
                    AppAppearance.entries.forEach { option ->
                        FilterChip(
                            selected = option == appearance, onClick = { onAppearance(option) },
                            label = { Text(option.name) }, modifier = Modifier.heightIn(min = 48.dp),
                        )
                    }
                }
                FlowRow(horizontalArrangement = Arrangement.spacedBy(VeritalexSpacing.small)) {
                    AppColorSource.entries.forEach { option ->
                        FilterChip(
                            selected = option == colorSource, onClick = { onColorSource(option) },
                            label = { Text(option.name) }, modifier = Modifier.heightIn(min = 48.dp),
                        )
                    }
                }
                if (Build.VERSION.SDK_INT < 31 && colorSource == AppColorSource.Dynamic) {
                    Text("Dynamic color requires Android 12; showing brand colors.")
                }
                Text("Scroll to inspect colors, actions, input, books, feedback, spacing, reader paper and the full type scale.")
                Box {
                    TextButton(onClick = { menu = true }, modifier = Modifier.heightIn(min = VeritalexLayout.minimumTouchTarget)) {
                        Text("Inspect: $section")
                    }
                    DropdownMenu(expanded = menu, onDismissRequest = { menu = false }) {
                        listOf("All", "Colors", "Actions", "Input", "Books", "Feedback", "Layout", "Reader", "Typography").forEach { option ->
                            DropdownMenuItem(
                                text = { Text(option) },
                                onClick = { section = option; menu = false },
                            )
                        }
                    }
                }
            }
        }
        if (section in listOf("All", "Colors")) item { ColorSpecimens() }
        if (section in listOf("All", "Actions")) item { ActionSpecimens() }
        if (section in listOf("All", "Input")) item { InputSpecimens() }
        if (section in listOf("All", "Books")) item { BookSpecimens() }
        if (section in listOf("All", "Feedback")) item { FeedbackSpecimens(onShowSnackbar) }
        if (section in listOf("All", "Layout")) item { LayoutSpecimens() }
        if (section in listOf("All", "Reader")) item { ReaderSpecimens() }
        if (section in listOf("All", "Typography")) item { TypographySpecimens() }
    }
}

@Composable
internal fun GallerySection(title: String, content: @Composable ColumnScope.() -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.compact)) {
        Text(title, style = MaterialTheme.typography.titleMedium, modifier = Modifier.semantics { heading() })
        content()
    }
}

@VeritalexPreviews
@Composable
private fun GalleryPreview() { DesignSystemGallery() }
