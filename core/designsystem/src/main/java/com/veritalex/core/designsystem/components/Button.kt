package com.veritalex.core.designsystem.components

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Image
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.tooling.preview.Preview
import com.veritalex.core.designsystem.theme.VeritalexTheme

@Composable
fun VerIconButton(
    onClick: () -> Unit,
    imageVector: ImageVector,
    contentDescription: String?,
    modifier: Modifier = Modifier,
) {
    IconButton(onClick = onClick) {
        Icon(imageVector = imageVector, contentDescription = contentDescription)
    }
}

@Preview(showBackground = true)
@Composable
fun PreviewVerIconButton() {
    VeritalexTheme {
        VerIconButton(
            onClick = { },
            imageVector = Icons.Filled.Image,
            contentDescription = null,
        )
    }
}
