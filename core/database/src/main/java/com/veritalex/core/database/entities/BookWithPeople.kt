package com.veritalex.core.database.entities

import androidx.room.Embedded
import androidx.room.Entity
import androidx.room.Relation

@Entity(primaryKeys = ["personId", "bookId"])
data class BookWithPeople(
    @Embedded val book: BookEntity,
    @Relation(
        entity = PersonEntity::class,
        parentColumn = "bookId",
        entityColumn = "personId"
    )
    val authors: List<PersonEntity>,
    @Relation(
        entity = PersonEntity::class,
        parentColumn = "bookId",
        entityColumn = "personId"
    )
    val translators: List<PersonEntity>
)
