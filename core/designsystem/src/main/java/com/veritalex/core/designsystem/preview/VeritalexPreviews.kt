package com.veritalex.core.designsystem.preview

import android.content.res.Configuration
import androidx.compose.ui.tooling.preview.Preview

/** Default phone canvas, with explicit light/dark rather than the IDE's current appearance. */
@Target(AnnotationTarget.ANNOTATION_CLASS, AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.BINARY)
@Preview(
    name = "Phone · light", group = "Veritalex · theme",
    widthDp = 412, heightDp = 915, showBackground = true,
    uiMode = Configuration.UI_MODE_NIGHT_NO,
)
@Preview(
    name = "Phone · dark", group = "Veritalex · theme",
    widthDp = 412, heightDp = 915, showBackground = true,
    uiMode = Configuration.UI_MODE_NIGHT_YES,
)
annotation class VeritalexThemePreviews

/** Narrow window at 200% text. Real Android font settings still need device checks. */
@Target(AnnotationTarget.ANNOTATION_CLASS, AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.BINARY)
@Preview(
    name = "Narrow · 200% · light", group = "Veritalex · large text",
    widthDp = 320, heightDp = 800, fontScale = 2f, showBackground = true,
    uiMode = Configuration.UI_MODE_NIGHT_NO,
)
@Preview(
    name = "Narrow · 200% · dark", group = "Veritalex · large text",
    widthDp = 320, heightDp = 800, fontScale = 2f, showBackground = true,
    uiMode = Configuration.UI_MODE_NIGHT_YES,
)
annotation class VeritalexLargeTextPreviews

/** Wider window for checking content measure and adaptive composition. */
@Target(AnnotationTarget.ANNOTATION_CLASS, AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.BINARY)
@Preview(
    name = "Tablet · light", group = "Veritalex · tablet",
    widthDp = 840, heightDp = 1000, showBackground = true,
    uiMode = Configuration.UI_MODE_NIGHT_NO,
)
@Preview(
    name = "Tablet · dark", group = "Veritalex · tablet",
    widthDp = 840, heightDp = 1000, showBackground = true,
    uiMode = Configuration.UI_MODE_NIGHT_YES,
)
annotation class VeritalexTabletPreviews

/** Six independent previews. Still wrap content in VeritalexTheme and Surface/Scaffold. */
@Target(AnnotationTarget.ANNOTATION_CLASS, AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.BINARY)
@VeritalexThemePreviews
@VeritalexLargeTextPreviews
@VeritalexTabletPreviews
annotation class VeritalexPreviews
