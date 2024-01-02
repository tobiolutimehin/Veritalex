package com.veritalex.core.data.repository

import androidx.paging.ExperimentalPagingApi
import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.PagingData
import androidx.paging.map
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import com.veritalex.core.database.VeritalexDatabase
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.database.entities.BookWithPeople
import com.veritalex.core.database.entities.PersonEntity
import com.veritalex.core.network.api.RetrofitNetworkDataSource
import com.veritalex.core.network.models.BookDto
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.withContext
import javax.inject.Inject

interface BooksRepository {
    fun fetchBooks(): Flow<PagingData<Book>>

    fun fetchRecommendedBooks(topic: String? = null): Flow<List<Book>>
}

@OptIn(ExperimentalPagingApi::class)
class OfflineFirstBooksRepository
    @Inject
    constructor(
        private val network: RetrofitNetworkDataSource,
        private val database: VeritalexDatabase,
        private val bookDao: BookDao,
    ) : BooksRepository {
        override fun fetchRecommendedBooks(topic: String?): Flow<List<Book>> {
            return bookDao.getRecommendedStream(topic).map { booksEntities ->
                booksEntities.map { bookEntity ->
                    bookEntity.toBook()
                }
            }.onEach { books ->
                if (books.isEmpty()) {
                    withContext(Dispatchers.IO) { getBooks() }
                }
            }
        }

        override fun fetchBooks(): Flow<PagingData<Book>> {
            return Pager(
                config =
                    PagingConfig(
                        pageSize = 100,
                    ),
                remoteMediator =
                    BooksRemoteMediator(
                        network = network,
                        bookDao = bookDao,
                    ),
            ) { bookDao.booksPagingSource() }.flow.map { pagingData ->
                pagingData.map { bookEntity ->
                    bookEntity.toBook()
                }
            }
        }

        suspend fun getBooks() {
            val response = network.getBooks()
            if (response.isSuccessful) {
                response.body()?.results?.insertBooks(bookDao)
            }
        }
    }

suspend fun List<BookDto>.insertBooks(bookDao: BookDao) {
    this.forEach { networkBook ->
        val bookEntity = networkBook.toBookEntity()
        val authors = networkBook.authors.map { it.toPersonEntity() }
        val translators =
            networkBook.translators?.map { it.toPersonEntity() } ?: emptyList()

        bookDao.insertBookWithPeople(bookEntity, authors, translators)
    }
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

fun PersonEntity.toPerson() =
    Person(
        name = this.name,
        deathYear = this.deathYear,
        birthYear = this.birthYear,
    )

fun List<PersonEntity>?.toPeople() = this?.map { it.toPerson() }
