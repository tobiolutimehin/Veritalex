package com.veritalex.core.network.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * A book from the Gutendex API.
 *
 * @property id The ID of the book.
 * @property title The title of the book.
 * @property subjects The subjects of the book.
 * @property authors The authors of the book.
 * @property translators The translators of the book.
 * @property bookshelves The bookshelves of the book.
 * @property languages The languages of the book.
 * @property mediaType The media type of the book.
 * @property formats The formats of the book.
 * @property downloadCount The download count of the book.
 * @property copyright if the book is copyrighted.
 * @constructor Creates a book.
 */
@Serializable
data class BookDto(
    val id: Int,
    val title: String,
    val subjects: List<String>,
    val authors: List<PersonDto>,
    val translators: List<PersonDto>? = null,
    val bookshelves: List<String>,
    val languages: List<String>,
    val copyright: Boolean? = null,
    @SerialName("media_type")
    val mediaType: String,
    val formats: Map<String, String>,
    @SerialName("download_count")
    val downloadCount: Int,
)
