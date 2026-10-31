package com.veritalex.core.designsystem.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import com.veritalex.core.designsystem.theme.VeritalexSpacing

/** Caller supplies factual status copy; color alone never communicates a state. */
@Composable
fun VeritalexProgress(label: String, progress: Float?, modifier: Modifier = Modifier) {
    val indicatorModifier = Modifier.fillMaxWidth().semantics { contentDescription = label }
    Column(modifier, verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.small)) {
        // The native indicator owns the label and range together, without a duplicate text stop.
        Text(label, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.clearAndSetSemantics {})
        if (progress == null) {
            LinearProgressIndicator(modifier = indicatorModifier)
        } else {
            LinearProgressIndicator(progress = { progress.coerceIn(0f, 1f) }, modifier = indicatorModifier)
        }
    }
}

/** Empty and retry states share layout, but their copy and action belong to the feature. */
@Composable
fun VeritalexMessage(
    title: String,
    message: String,
    modifier: Modifier = Modifier,
    action: @Composable (() -> Unit)? = null,
) {
    Column(
        modifier = modifier.padding(vertical = VeritalexSpacing.large),
        verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.compact),
    ) {
        Text(title, style = MaterialTheme.typography.titleMedium, modifier = Modifier.semantics { heading() })
        Text(message, style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
        action?.invoke()
    }
}
