package com.veritalex.core.designsystem.gallery

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.semantics.Role
import com.veritalex.core.designsystem.R
import com.veritalex.core.designsystem.preview.VeritalexLargeTextPreviews
import com.veritalex.core.designsystem.preview.VeritalexThemePreviews
import com.veritalex.core.designsystem.components.ActionStyle
import com.veritalex.core.designsystem.components.VeritalexButton
import com.veritalex.core.designsystem.components.VeritalexIconButton
import com.veritalex.core.designsystem.components.VeritalexMessage
import com.veritalex.core.designsystem.components.VeritalexProgress
import com.veritalex.core.designsystem.components.VeritalexSearchField
import com.veritalex.core.designsystem.components.VeritalexTextField
import com.veritalex.core.designsystem.theme.VeritalexLayout
import com.veritalex.core.designsystem.theme.VeritalexSpacing
import com.veritalex.core.designsystem.theme.VeritalexTheme

@Composable
internal fun ActionSpecimens() {
    var activations by remember { mutableIntStateOf(0) }
    GallerySection("Actions") {
        Text("Activations: $activations · only ready actions respond")
        ActionStyle.entries.forEach { style ->
            val label = if (style == ActionStyle.Destructive) "Remove example" else "Save book"
            Text(style.name, style = MaterialTheme.typography.titleSmall)
            VeritalexButton(label, { activations++ }, style = style, modifier = Modifier.fillMaxWidth())
            VeritalexButton("$label · disabled", {}, style = style, enabled = false, modifier = Modifier.fillMaxWidth())
            VeritalexButton("$label · in progress", {}, style = style, loading = true, modifier = Modifier.fillMaxWidth())
        }
        Text("Icon actions: ready, disabled, busy")
        Row(horizontalArrangement = Arrangement.spacedBy(VeritalexSpacing.small)) {
            VeritalexIconButton("Close example", { activations++ }) { CloseIcon() }
            VeritalexIconButton("Close unavailable", {}, enabled = false) { CloseIcon() }
            VeritalexIconButton("Closing example", {}, loading = true) { CloseIcon() }
        }
        VeritalexButton(
            "A long action label that should reflow at enlarged text sizes", { activations++ },
            modifier = Modifier.fillMaxWidth(),
        )
    }
}

@VeritalexThemePreviews
@VeritalexLargeTextPreviews
@Composable
private fun ActionsPreview() {
    VeritalexTheme {
        Surface {
            Column(Modifier.verticalScroll(rememberScrollState()).padding(VeritalexSpacing.medium)) { ActionSpecimens() }
        }
    }
}

@VeritalexThemePreviews
@VeritalexLargeTextPreviews
@Composable
private fun InputPreview() {
    VeritalexTheme {
        Surface {
            Column(Modifier.verticalScroll(rememberScrollState()).padding(VeritalexSpacing.medium)) { InputSpecimens() }
        }
    }
}

@Composable
private fun CloseIcon() { Icon(painterResource(R.drawable.ic_close), contentDescription = null) }

@Composable
internal fun InputSpecimens() {
    var text by rememberSaveable { mutableStateOf("") }
    var query by rememberSaveable { mutableStateOf("Austen") }
    var selected by rememberSaveable { mutableStateOf(true) }
    var checked by rememberSaveable { mutableStateOf(false) }
    var choice by rememberSaveable { mutableStateOf("Comfortable") }
    GallerySection("Input and selection") {
        VeritalexTextField(text, { text = it }, "Shelf name", supportingText = "A short, memorable name")
        VeritalexTextField("", {}, "Shelf name", error = "Enter a name to continue.")
        VeritalexTextField("Unavailable example", {}, "Shelf name", enabled = false)
        VeritalexSearchField(query, { query = it }, {}, "Search books")
        FlowRow(horizontalArrangement = Arrangement.spacedBy(VeritalexSpacing.small)) {
            FilterChip(selected, { selected = !selected }, label = { Text("Downloaded") }, modifier = Modifier.heightIn(min = VeritalexLayout.minimumTouchTarget))
            FilterChip(false, {}, enabled = false, label = { Text("Unavailable") }, modifier = Modifier.heightIn(min = VeritalexLayout.minimumTouchTarget))
        }
        Row(
            Modifier.fillMaxWidth().heightIn(min = VeritalexLayout.minimumTouchTarget)
                .toggleable(checked, role = Role.Switch, onValueChange = { checked = it }),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text("Example preference", Modifier.weight(1f))
            Switch(checked, onCheckedChange = null)
        }
        Column(Modifier.selectableGroup()) {
          listOf("Comfortable", "Compact").forEach { option ->
            Row(
                Modifier.fillMaxWidth().heightIn(min = VeritalexLayout.minimumTouchTarget)
                    .selectable(choice == option, role = Role.RadioButton, onClick = { choice = option }),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(VeritalexSpacing.small),
            ) {
                RadioButton(choice == option, onClick = null)
                Text(option)
            }
          }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
internal fun FeedbackSpecimens(onShowSnackbar: () -> Unit) {
    var dialog by rememberSaveable { mutableStateOf(false) }
    var sheet by rememberSaveable { mutableStateOf(false) }
    GallerySection("Feedback and overlays") {
        Surface(color = MaterialTheme.colorScheme.tertiaryContainer, shape = MaterialTheme.shapes.small) {
            Text("Reading · status example", Modifier.padding(VeritalexSpacing.small), color = MaterialTheme.colorScheme.onTertiaryContainer)
        }
        VeritalexProgress("Sample progress · 28%", 0.28f)
        VeritalexProgress("Loading example", null)
        VeritalexMessage("No books yet", "Saved books will appear here.")
        VeritalexMessage("Couldn’t load books", "Check your connection and try again.") {
            VeritalexButton("Retry example", {}, style = ActionStyle.Secondary)
        }
        HorizontalDivider()
        VeritalexButton("Show dialog", { dialog = true }, style = ActionStyle.Outlined)
        VeritalexButton("Show sheet", { sheet = true }, style = ActionStyle.Outlined)
        VeritalexButton("Show snackbar", onShowSnackbar, style = ActionStyle.Ghost)
    }
    if (dialog) {
        AlertDialog(
            onDismissRequest = { dialog = false },
            title = { Text("Remove example?") },
            text = { Text("This gallery demonstrates confirmation styling. No book or data will be removed.") },
            confirmButton = { VeritalexButton("Remove example", { dialog = false }, style = ActionStyle.Destructive) },
            dismissButton = { VeritalexButton("Cancel", { dialog = false }, style = ActionStyle.Ghost) },
        )
    }
    if (sheet) {
        ModalBottomSheet(onDismissRequest = { sheet = false }) {
            Column(Modifier.padding(VeritalexSpacing.large), verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.medium)) {
                Text("Example sheet", style = MaterialTheme.typography.titleLarge)
                Text("Native drag, Back, focus, scrim and inset handling. No settings are saved.")
                VeritalexButton("Done", { sheet = false }, modifier = Modifier.fillMaxWidth())
            }
        }
    }
}
