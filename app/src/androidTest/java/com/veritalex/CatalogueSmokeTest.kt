package com.veritalex

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class CatalogueSmokeTest {
    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun launchDisplaysTheSampleCatalogue() {
        composeRule.onNodeWithText("Sample catalogue").assertIsDisplayed()
        composeRule.onNodeWithText("Pride and Prejudice").assertIsDisplayed()
        composeRule.onNodeWithText("Jane Austen").assertIsDisplayed()
    }
}
