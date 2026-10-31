package com.veritalex.core.designsystem.components

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.error
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.input.ImeAction
import com.veritalex.core.designsystem.R

/** Error copy describes a recovery, not only a red outline. State stays with the caller. */
@Composable
fun VeritalexTextField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier,
    supportingText: String? = null,
    error: String? = null,
    enabled: Boolean = true,
    singleLine: Boolean = false,
) {
    val supporting = error ?: supportingText
    OutlinedTextField(
        value = value, onValueChange = onValueChange,
        label = { Text(label) },
        supportingText = supporting?.let { { Text(it) } },
        isError = error != null, enabled = enabled, singleLine = singleLine,
        shape = MaterialTheme.shapes.medium,
        modifier = modifier.fillMaxWidth().semantics { if (error != null) error(error) },
    )
}

/** Inline search without suggestions; use native SearchBar when expansion/results are required. */
@Composable
fun VeritalexSearchField(
    query: String,
    onQueryChange: (String) -> Unit,
    onSearch: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
) {
    OutlinedTextField(
        value = query, onValueChange = onQueryChange,
        label = { Text(label) }, singleLine = true, enabled = enabled,
        shape = MaterialTheme.shapes.medium,
        leadingIcon = { Icon(painterResource(R.drawable.ic_search), contentDescription = null) },
        trailingIcon = if (query.isNotEmpty()) {
            {
                VeritalexIconButton(
                    label = stringResource(R.string.clear_search),
                    onClick = { onQueryChange("") }, enabled = enabled,
                ) { Icon(painterResource(R.drawable.ic_close), contentDescription = null) }
            }
        } else null,
        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
        keyboardActions = KeyboardActions(onSearch = { if (enabled) onSearch(query) }),
        modifier = modifier.fillMaxWidth(),
    )
}
