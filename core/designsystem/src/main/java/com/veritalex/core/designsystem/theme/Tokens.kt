package com.veritalex.core.designsystem.theme

import androidx.compose.runtime.Composable
import androidx.compose.ui.res.dimensionResource
import androidx.compose.ui.unit.dp
import com.veritalex.core.designsystem.R

/** Gaps and padding, not fixed heights for text-bearing controls. */
object VeritalexSpacing {
    val extraSmall = 4.dp
    val small = 8.dp
    val compact = 12.dp
    val medium = 16.dp
    val large = 24.dp
    val extraLarge = 32.dp
}

object VeritalexLayout {
    val minimumTouchTarget = 48.dp
    val contentMaxWidth = 720.dp
    val readerMaxWidth = 680.dp
    val listCoverWidth = 64.dp

    // Resources adapt to the available window: 16dp below 400dp, otherwise 20dp.
    val gutter @Composable get() = dimensionResource(R.dimen.content_gutter)
}
