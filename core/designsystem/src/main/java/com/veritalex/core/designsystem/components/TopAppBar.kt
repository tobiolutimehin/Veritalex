package com.veritalex.core.designsystem.components

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarColors
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.tooling.preview.Preview
import com.veritalex.core.designsystem.icons.VeritalexIcons
import com.veritalex.core.designsystem.theme.VeritalexTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VerTopAppBar(
    title: String,
    modifier: Modifier = Modifier,
    navigationIcon: ImageVector = VeritalexIcons.ArrowBack,
    navigationIconContentDescription: String? = null,
    actionIcon: ImageVector = VeritalexIcons.MoreVert,
    actionIconContentDescription: String? = null,
    colors: TopAppBarColors = TopAppBarDefaults.centerAlignedTopAppBarColors(),
    onNavigationClick: () -> Unit = {},
    onActionClick: () -> Unit = {},
) {
    TopAppBar(
        title = {
            Text(text = title, style = MaterialTheme.typography.titleLarge)
        },
        navigationIcon = {
            VerIconButton(
                onClick = onNavigationClick,
                imageVector = navigationIcon,
                contentDescription = navigationIconContentDescription,
            )
        },
        actions = {
            VerIconButton(
                onClick = onActionClick,
                imageVector = actionIcon,
                contentDescription = actionIconContentDescription,
            )
        },
        modifier = modifier.testTag("veritalexTopAppBar"),
        colors = colors,
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Preview
@Composable
private fun VeritalexTopAppBarPreview() {
    VeritalexTheme {
        VerTopAppBar(title = "Veritalex")
    }
}
