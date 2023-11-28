package com.veritalex.core.database.entities

import androidx.room.Embedded
import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.Relation

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

@Entity(tableName = "favorites")
data class FavoriteEntity(
    @PrimaryKey(autoGenerate = true)
    val favoriteId: Int,
    val bookId: Int,
)

@Entity(primaryKeys = ["bookId", "bookId"])
data class FavoriteBook(
    @Embedded val favorite: FavoriteEntity,
    @Relation(
        entity = BookEntity::class,
        parentColumn = "bookId",
        entityColumn = "bookId"
    )
    val book: BookEntity,
)