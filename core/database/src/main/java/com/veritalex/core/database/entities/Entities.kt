package com.veritalex.core.database.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "books")
data class RoomEntity(
    @PrimaryKey
    val id: Int,
    val title: String,
    val subjects: List<String>,
    val bookshelves: List<String>,
    val languages: List<String>,
    val copyright: Boolean?,
    val mediaType: String,
    val downloadCount: Int,
)

@Entity(tableName = "formats")
data class RoomFormat(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val formatKey: String,
    val formatValue: String,
    val bookId: Int, // Foreign key to associate formats with books
)

@Entity(tableName = "persons")
data class PersonEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val birthYear: Int?,
    val deathYear: Int?,
    val name: String,
    val bookId: Int, // Foreign key to associate persons with books
)
