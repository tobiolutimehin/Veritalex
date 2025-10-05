package com.veritalex.feature.home.navigation

import androidx.annotation.DrawableRes
import androidx.annotation.StringRes
import com.veritalex.feature.home.R

data class TabItem(
    @StringRes val title: Int,
    @DrawableRes val icon: Int? = null,
) {
    companion object {
        val tabsList =
            listOf(
                TabItem(
                    R.string.home,
                ),
                TabItem(
                    R.string.my_saved_books,
                ),
            )
    }
}