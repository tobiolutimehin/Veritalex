package com.veritalex.core.database.entities

import androidx.room.Embedded
import androidx.room.Junction
import androidx.room.Relation

data class BookWithPeople(
    @Embedded val book: BookEntity,
    @Relation(
        entity = PersonEntity::class,
        parentColumn = "bookId",
        entityColumn = "personId",
        associateBy = Junction(BookAuthorCrossRef::class),
    )
    val authors: List<PersonEntity>,
    @Relation(
        entity = PersonEntity::class,
        parentColumn = "bookId",
        entityColumn = "personId",
        associateBy = Junction(BookTranslatorCrossRef::class),
    )
    val translators: List<PersonEntity>
)
