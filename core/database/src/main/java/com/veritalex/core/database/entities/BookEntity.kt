package com.veritalex.core.database.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "books")
data class BookEntity(
    @PrimaryKey
    val bookId: Int,
    val title: String,
    val subjects: List<String>,
    val bookshelves: List<String>,
    val languages: List<String>,
    val copyright: Boolean?,
    val mediaType: String,
    val downloadCount: Int,
    val formats: Map<String, String>
)