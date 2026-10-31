package com.veritalex

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertIsSelected
import androidx.compose.ui.test.hasText
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollToNode
import android.view.KeyEvent
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Rule
import org.junit.Test
import org.junit.Assert.assertFalse
import android.view.WindowInsetsController

class GalleryInteractionTest {
    @get:Rule val rule = createAndroidComposeRule<DesignSystemGalleryActivity>()

    @Test fun appearanceChoicesAndNativeOverlaysWorkInTheGallery() {
        rule.onNodeWithText("Dark").performClick().assertIsSelected()
        rule.runOnIdle {
            val activity = rule.activity
            val appearance = activity.window.insetsController!!.systemBarsAppearance
            assertFalse(appearance and WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS != 0)
        }
        rule.onNodeWithText("Dynamic").performClick().assertIsSelected()
        rule.onNodeWithText("Inspect: All").performClick()
        rule.onNodeWithText("Feedback").performClick()
        val gallery = rule.onNodeWithTag("gallery")
        gallery.performScrollToNode(hasText("Show dialog"))
        rule.onNodeWithText("Show dialog").performClick()
        rule.onNodeWithText("Remove example?").assertIsDisplayed()
        rule.onNodeWithText("Cancel").performClick()
        rule.onNodeWithText("Remove example?").assertDoesNotExist()
        gallery.performScrollToNode(hasText("Show sheet"))
        rule.onNodeWithText("Show sheet").performClick()
        rule.onNodeWithText("Example sheet").assertIsDisplayed()
        InstrumentationRegistry.getInstrumentation().sendKeyDownUpSync(KeyEvent.KEYCODE_BACK)
        rule.onNodeWithText("Example sheet").assertDoesNotExist()
        gallery.performScrollToNode(hasText("Show snackbar"))
        rule.onNodeWithText("Show snackbar").performClick()
        rule.onNodeWithText("Example feedback").assertIsDisplayed()
    }
}
