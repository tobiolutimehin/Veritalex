package com.veritalex.core.designsystem

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VeritalexTopAppBar(
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
            IconButton(onClick = onNavigationClick) {
                Icon(imageVector = navigationIcon, contentDescription = navigationIconContentDescription)
            }
        },
        actions = {
            IconButton(onClick = onActionClick) {
                Icon(imageVector = actionIcon, contentDescription = actionIconContentDescription)
            }
        },
        modifier = modifier.testTag("veritalexTopAppBar"),
        colors = colors,
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Preview
@Composable
private fun VeritalexTopAppBarPreview() {
//    VeritalexTheme {
        VeritalexTopAppBar(title = "Veritalex")
//    }
}