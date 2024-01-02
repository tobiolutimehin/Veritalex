package com.veritalex.core.data.utils

import com.veritalex.core.data.utils.ModelConverters.toBookEntity
import com.veritalex.core.data.utils.ModelConverters.toPersonEntity
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.network.models.BookDto

object Extensions {
    suspend fun List<BookDto>.insertBooks(bookDao: BookDao) {
        this.forEach { networkBook ->
            val bookEntity = networkBook.toBookEntity()
            val authors = networkBook.authors.map { it.toPersonEntity() }
            val translators =
                networkBook.translators?.map { it.toPersonEntity() } ?: emptyList()

            bookDao.insertBookWithPeople(bookEntity, authors, translators)
        }
    }
}
