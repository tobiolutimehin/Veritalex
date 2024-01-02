package com.veritalex.core.data.repository

import androidx.paging.ExperimentalPagingApi
import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.PagingData
import androidx.paging.map
import com.veritalex.core.data.models.Book
import com.veritalex.core.data.utils.Extensions.insertBooks
import com.veritalex.core.data.utils.ModelConverters.toBook
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.network.api.RetrofitNetworkDataSource
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

        private suspend fun getBooks() {
            val response = network.getBooks()
            if (response.isSuccessful) {
                response.body()?.results?.insertBooks(bookDao)
            }
        }
    }
