package com.veritalex.core.network.models

import kotlinx.serialization.Serializable

/**
 * Represents the response format for a list of books obtained from the Gutendex API.
 *
 * @property count The total number of books for the query on all pages combined.
 * @property next URL to the next page of results, or null if there is no next page.
 * @property previous URL to the previous page of results, or null if there is no previous page.
 * @property results List of [BookDto] objects representing individual books in the response.
 */
@Serializable
data class BookListResponse(
    val count: Int,
    val next: String?,
    val previous: String?,
    val results: List<BookDto>,
)
