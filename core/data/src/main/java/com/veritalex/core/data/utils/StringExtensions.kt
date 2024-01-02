package com.veritalex.core.data.utils

object StringExtensions {
    fun String.extractPageNumberFromUrl(): Int? {
        val regex = Regex("""[?&]page=(\d+)""")
        val matchResult = regex.find(this)
        return matchResult?.groupValues?.get(1)?.toIntOrNull()
    }
}
