package com.veritalex.core.data.utils

import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import com.veritalex.core.database.entities.BookEntity
import com.veritalex.core.database.entities.BookWithPeople
import com.veritalex.core.database.entities.PersonEntity
import com.veritalex.core.network.models.BookDto
import com.veritalex.core.network.models.PersonDto

object ModelConverters {
    fun PersonDto.toPersonEntity(): PersonEntity {
        return PersonEntity(
            birthYear = this.birthYear,
            deathYear = this.deathYear,
            name = this.name,
        )
    }

    fun BookDto.toBookEntity(): BookEntity {
        return BookEntity(
            bookId = this.id,
            title = this.title,
            subjects = this.subjects,
            bookshelves = this.bookshelves,
            languages = this.languages,
            copyright = this.copyright,
            mediaType = this.mediaType,
            formats = this.formats,
            downloadCount = this.downloadCount,
        )
    }

    fun BookWithPeople.toBook(): Book {
        val book = this.book
        return Book(
            id = book.bookId,
            title = book.title,
            subjects = book.subjects,
            authors = this.authors.toPeople(),
            translators = this.translators.toPeople(),
            bookshelves = book.bookshelves,
            languages = book.languages,
            copyright = book.copyright,
            mediaType = book.mediaType,
            formats = book.formats,
            downloadCount = book.downloadCount,
        )
    }

    private fun PersonEntity.toPerson() =
        Person(
            name = this.name,
            deathYear = this.deathYear,
            birthYear = this.birthYear,
        )

    private fun List<PersonEntity>.toPeople() = this.map { it.toPerson() }
}
