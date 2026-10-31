package com.veritalex.core.database.entities

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index

@Entity(
    tableName = "book_translators",
    primaryKeys = ["bookId", "personId"],
    indices = [Index("personId")],
    foreignKeys = [
        ForeignKey(entity = BookEntity::class, parentColumns = ["bookId"], childColumns = ["bookId"], onDelete = ForeignKey.CASCADE),
        ForeignKey(entity = PersonEntity::class, parentColumns = ["personId"], childColumns = ["personId"], onDelete = ForeignKey.CASCADE),
    ],
)
data class BookTranslatorCrossRef(val bookId: Int, val personId: Long)
