package com.veritalex.core.data.repository

import androidx.paging.ExperimentalPagingApi
import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.PagingData
import androidx.paging.map
import com.veritalex.core.data.BooksRemoteMediator
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.models.Person
import com.veritalex.core.database.VeritalexDatabase
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.database.entities.BookWithPeople
import com.veritalex.core.database.entities.PersonEntity
import com.veritalex.core.network.api.RetrofitNetworkDataSource
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject

interface BooksRepository {
    suspend fun fetchBooks(): Flow<PagingData<Book>>

    fun fetchBookById(id: Int)
}

@OptIn(ExperimentalPagingApi::class)
class OfflineFirstBooksRepository @Inject constructor(
    private val network: RetrofitNetworkDataSource,
    private val database: VeritalexDatabase,
    private val bookDao: BookDao
) : BooksRepository {

    override fun fetchBookById(id: Int) {
        TODO("Not yet implemented")
    }

    override suspend fun fetchBooks(): Flow<PagingData<Book>> {
        return Pager(
            config = PagingConfig(
                pageSize = 100
            ),
            remoteMediator = BooksRemoteMediator(
                network = network, bookDao = bookDao
            )
        ) { bookDao.booksPagingSource() }.flow.map { pagingData ->
            pagingData.map { bookEntity ->
                bookEntity.toBook()
            }
        }
    }
}

fun BookWithPeople.toBook(): Book {
    val book = this.book
    return Book(
        id = book.bookId,
        title = book.title,
        subjects = book.subjects,
        authors = this.authors.toPeople() , // You may need to fetch authors separately
        translators = this.translators.toPeople(), // You may need to fetch translators separately
        bookshelves = book.bookshelves,
        languages = book.languages,
        copyright = book.copyright,
        mediaType = book.mediaType,
        formats = book.formats,
        downloadCount = book.downloadCount
    )
}

fun PersonEntity.toPerson() = Person(
    name = this.name,
    deathYear = this.deathYear,
    birthYear = this.birthYear
)

fun List<PersonEntity>?.toPeople() = this?.map { it.toPerson() } ?: emptyList()