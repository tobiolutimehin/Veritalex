package com.veritalex.core.designsystem.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.sizeIn
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ButtonColors
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.IconButton
import androidx.compose.material3.IconButtonDefaults
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.unit.dp
import com.veritalex.core.designsystem.R
import com.veritalex.core.designsystem.theme.VeritalexLayout
import com.veritalex.core.designsystem.theme.VeritalexSpacing

enum class ActionStyle { Primary, Secondary, Outlined, Ghost, Destructive }

/** A ghost action is a native Material TextButton. The caller owns in-flight state. */
@Composable
fun VeritalexButton(
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    style: ActionStyle = ActionStyle.Primary,
    enabled: Boolean = true,
    loading: Boolean = false,
) {
    val busyLabel = stringResource(R.string.action_loading)
    val actionModifier = modifier
        .heightIn(min = VeritalexLayout.minimumTouchTarget)
        .semantics { if (loading) stateDescription = busyLabel }
    val activate = { if (enabled && !loading) onClick() }
    val content: @Composable () -> Unit = {
        Row(
            horizontalArrangement = Arrangement.spacedBy(VeritalexSpacing.small),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            if (loading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(18.dp).clearAndSetSemantics {},
                    color = LocalContentColor.current,
                    strokeWidth = 2.dp,
                )
            }
            Text(label, style = MaterialTheme.typography.labelLarge)
        }
    }
    when (style) {
        ActionStyle.Primary -> Button(
            onClick = activate, enabled = enabled && !loading, modifier = actionModifier,
            colors = ButtonDefaults.buttonColors().duringLoading(loading && enabled),
        ) { content() }
        ActionStyle.Secondary -> FilledTonalButton(
            onClick = activate, enabled = enabled && !loading, modifier = actionModifier,
            colors = ButtonDefaults.filledTonalButtonColors().duringLoading(loading && enabled),
        ) { content() }
        ActionStyle.Outlined -> OutlinedButton(
            onClick = activate, enabled = enabled && !loading, modifier = actionModifier,
            colors = ButtonDefaults.outlinedButtonColors().duringLoading(loading && enabled),
            border = ButtonDefaults.outlinedButtonBorder(enabled),
        ) { content() }
        ActionStyle.Ghost -> TextButton(
            onClick = activate, enabled = enabled && !loading, modifier = actionModifier,
            colors = ButtonDefaults.textButtonColors().duringLoading(loading && enabled),
        ) { content() }
        ActionStyle.Destructive -> Button(
            onClick = activate, enabled = enabled && !loading, modifier = actionModifier,
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.error,
                contentColor = MaterialTheme.colorScheme.onError,
            ).duringLoading(loading && enabled),
        ) { content() }
    }
}

// Busy is unavailable for activation, but remains legible and distinct from an unavailable action.
private fun ButtonColors.duringLoading(loading: Boolean): ButtonColors = if (loading) {
    copy(disabledContainerColor = containerColor, disabledContentColor = contentColor)
} else this

@Composable
fun VeritalexIconButton(
    label: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    loading: Boolean = false,
    icon: @Composable () -> Unit,
) {
    val busyLabel = stringResource(R.string.action_loading)
    val colors = IconButtonDefaults.iconButtonColors()
    IconButton(
        onClick = { if (enabled && !loading) onClick() },
        enabled = enabled && !loading,
        colors = if (loading && enabled) colors.copy(
            disabledContainerColor = colors.containerColor, disabledContentColor = colors.contentColor,
        ) else colors,
        modifier = modifier.sizeIn(
            minWidth = VeritalexLayout.minimumTouchTarget,
            minHeight = VeritalexLayout.minimumTouchTarget,
        ).semantics {
            contentDescription = label
            if (loading) stateDescription = busyLabel
        },
    ) {
        androidx.compose.foundation.layout.Box(Modifier.clearAndSetSemantics {}) {
            if (loading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp), color = LocalContentColor.current, strokeWidth = 2.dp,
                )
            } else {
                icon()
            }
        }
    }
}
