package com.veritalex

import androidx.activity.compose.setContent
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.SideEffect
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Density
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.SemanticsActions
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.semantics.ProgressBarRangeInfo
import androidx.compose.ui.test.SemanticsMatcher
import androidx.compose.ui.test.assert
import androidx.compose.ui.test.assertCountEquals
import androidx.compose.ui.test.hasContentDescription
import androidx.compose.ui.test.hasText
import androidx.compose.ui.test.assertContentDescriptionEquals
import androidx.compose.ui.test.assertWidthIsAtLeast
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performSemanticsAction
import androidx.compose.ui.test.performTextReplacement
import androidx.compose.ui.text.TextLayoutResult
import androidx.compose.ui.Modifier
import androidx.compose.ui.test.assertIsEnabled
import androidx.compose.ui.test.assertIsNotEnabled
import androidx.compose.ui.test.assertTextEquals
import androidx.compose.ui.test.assertHeightIsAtLeast
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performTouchInput
import androidx.compose.ui.test.click
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import com.veritalex.core.designsystem.components.ActionStyle
import com.veritalex.core.designsystem.components.VeritalexButton
import com.veritalex.core.designsystem.components.VeritalexIconButton
import com.veritalex.core.designsystem.components.VeritalexTextField
import com.veritalex.core.designsystem.components.VeritalexSearchField
import com.veritalex.core.designsystem.components.VeritalexProgress
import com.veritalex.core.designsystem.components.BookListRow
import com.veritalex.core.designsystem.theme.AppAppearance
import com.veritalex.core.designsystem.theme.AppColorSource
import com.veritalex.core.designsystem.theme.ReaderTheme
import com.veritalex.core.designsystem.theme.ReaderPaper
import com.veritalex.core.designsystem.theme.colors
import com.veritalex.core.designsystem.theme.VeritalexTheme
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Rule
import org.junit.Test

class DesignSystemBehaviorTest {
    @get:Rule val rule = createAndroidComposeRule<MainActivity>()

    @Test fun everyActionKeepsItsLabelAndBlocksActivationWhileLoadingOrDisabled() {
        val style = mutableStateOf(ActionStyle.Primary)
        val loading = mutableStateOf(false)
        val enabled = mutableStateOf(true)
        var calls = 0
        rule.runOnUiThread {
            rule.activity.setContent {
                VeritalexTheme {
                    VeritalexButton(
                        label = "Save book", onClick = { calls++ }, style = style.value,
                        loading = loading.value, enabled = enabled.value,
                        modifier = Modifier.testTag("action"),
                    )
                }
            }
        }
        ActionStyle.entries.forEach { variant ->
            rule.runOnIdle { style.value = variant; loading.value = false; enabled.value = true }
            val action = rule.onNodeWithTag("action")
            action.assertIsEnabled().assertHeightIsAtLeast(48.dp).assertTextEquals("Save book")
            action.performTouchInput { click() }
            rule.runOnIdle { assertEquals(1, calls); loading.value = true }
            action.assertIsNotEnabled().assertTextEquals("Save book")
                .assert(SemanticsMatcher.expectValue(SemanticsProperties.StateDescription, "In progress"))
            action.performTouchInput { click() }
            rule.runOnIdle { assertEquals(1, calls); loading.value = false; enabled.value = false }
            action.assertIsNotEnabled().performTouchInput { click() }
            rule.runOnIdle { assertEquals(1, calls); calls = 0 }
        }
    }

    private fun show(content: @Composable () -> Unit) {
        rule.runOnUiThread {
            rule.activity.setContent { VeritalexTheme { Surface { content() } } }
        }
    }

    @Test fun progressHasOneAccessibleNodeWithItsLabelAndRange() {
        val progress = mutableStateOf<Float?>(0.28f)
        val label = "Sample progress"
        show { VeritalexProgress(label, progress.value) }

        val namedProgress = hasText(label) or hasContentDescription(label)
        rule.onNode(namedProgress).assert(
            SemanticsMatcher.expectValue(
                SemanticsProperties.ProgressBarRangeInfo, ProgressBarRangeInfo(0.28f, 0f..1f),
            ),
        )
        rule.onAllNodes(namedProgress).assertCountEquals(1)
        rule.onAllNodes(SemanticsMatcher.keyIsDefined(SemanticsProperties.ProgressBarRangeInfo)).assertCountEquals(1)

        rule.runOnIdle { progress.value = null }
        rule.onNode(namedProgress).assert(
            SemanticsMatcher.expectValue(
                SemanticsProperties.ProgressBarRangeInfo, ProgressBarRangeInfo.Indeterminate,
            ),
        )
        rule.onAllNodes(namedProgress).assertCountEquals(1)
        rule.onAllNodes(SemanticsMatcher.keyIsDefined(SemanticsProperties.ProgressBarRangeInfo)).assertCountEquals(1)
    }

    @Test fun iconActionsHaveLabelsTargetsAndBusyProtection() {
        val busy = mutableStateOf(false)
        var calls = 0
        show {
            VeritalexIconButton("Close example", { calls++ }, loading = busy.value) { Text("×") }
        }
        val icon = rule.onNodeWithContentDescription("Close example")
        icon.assertHeightIsAtLeast(48.dp).assertWidthIsAtLeast(48.dp).performClick()
        rule.runOnIdle { assertEquals(1, calls); busy.value = true }
        icon.assertContentDescriptionEquals("Close example").assertIsNotEnabled()
        icon.performTouchInput { click() }
        rule.runOnIdle { assertEquals(1, calls) }
    }

    @Test fun fieldErrorsExplainRecoveryAndSearchClearUpdatesTheCaller() {
        val name = mutableStateOf("")
        val query = mutableStateOf("Austen")
        show {
            Column {
                VeritalexTextField(name.value, { name.value = it }, "Shelf name", error = "Enter a name to continue.", modifier = Modifier.testTag("field"))
                VeritalexSearchField(query.value, { query.value = it }, {}, "Search books")
            }
        }
        rule.onNodeWithTag("field")
            .assert(SemanticsMatcher.expectValue(SemanticsProperties.Error, "Enter a name to continue."))
            .performTextReplacement("Favourites")
        rule.runOnIdle { assertEquals("Favourites", name.value) }
        rule.onNodeWithContentDescription("Clear search").performClick()
        rule.runOnIdle { assertEquals("", query.value) }
        rule.onNodeWithContentDescription("Clear search").assertDoesNotExist()
    }

    @Test fun bookMetadataAndLongActionsReflowAt200PercentIn280Dp() {
        val title = "A deliberately long book title that must remain fully readable across several lines"
        val label = "A long action label that needs room to wrap naturally"
        show {
            CompositionLocalProvider(LocalDensity provides Density(LocalDensity.current.density, 2f)) {
                Column(Modifier.width(280.dp).verticalScroll(rememberScrollState())) {
                    BookListRow(title, "An author with a long name")
                    VeritalexButton(label, {})
                }
            }
        }
        listOf(title, label).forEach { text ->
            val layouts = mutableListOf<TextLayoutResult>()
            rule.onNodeWithText(text).performSemanticsAction(SemanticsActions.GetTextLayoutResult) { it(layouts) }
            rule.runOnIdle {
                org.junit.Assert.assertTrue("No text layout for $text", layouts.isNotEmpty())
                layouts.forEach { assertFalse("Clipped text: $text", it.hasVisualOverflow) }
            }
        }
    }

    @Test fun readerPaperStaysIndependentOfAppAppearanceAndDynamicColor() {
        val appearance = mutableStateOf(AppAppearance.Light)
        val source = mutableStateOf(AppColorSource.Brand)
        var paperColor = Color.Unspecified
        var interfaceColor = Color.Unspecified
        rule.runOnUiThread {
            rule.activity.setContent {
                VeritalexTheme(appearance.value, source.value) {
                    val appSurface = MaterialTheme.colorScheme.surface
                    ReaderTheme(ReaderPaper.Sepia) {
                        val paper = ReaderTheme.colors.background
                        SideEffect { paperColor = paper; interfaceColor = appSurface }
                    }
                }
            }
        }
        rule.runOnIdle { assertEquals(ReaderPaper.Sepia.colors().background, paperColor); appearance.value = AppAppearance.Dark }
        rule.runOnIdle {
            assertEquals(ReaderPaper.Sepia.colors().background, paperColor)
            assertEquals(Color(0xFF19120D), interfaceColor)
            source.value = AppColorSource.Dynamic
        }
        rule.runOnIdle { assertEquals(ReaderPaper.Sepia.colors().background, paperColor) }
    }
}
