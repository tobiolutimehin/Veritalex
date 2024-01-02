package com.veritalex.core.data.models

/**
 * Represents information about a book.
 *
 * @property id The unique identifier of the book.
 * @property title The title of the book.
 * @property subjects The list of subjects associated with the book.
 * @property authors The list of authors of the book.
 * @property translators The list of translators of the book. Can be null if there are none.
 * @property bookshelves The list of bookshelves to which the book belongs.
 * @property languages The list of languages in which the book is available.
 * @property copyright The copyright status of the book. Can be null if information is not available.
 * @property mediaType The media type of the book.
 * @property formats The map of MIME types to their corresponding URLs.
 * @property downloadCount The number of times the book has been downloaded.
 */
data class Book(
    val id: Int,
    val title: String,
    val subjects: List<String>,
    val authors: List<Person>?,
    val translators: List<Person>?,
    val bookshelves: List<String>,
    val languages: List<String>,
    val copyright: Boolean?,
    val mediaType: String,
    val formats: Map<String, String>,
    val downloadCount: Int,
)
