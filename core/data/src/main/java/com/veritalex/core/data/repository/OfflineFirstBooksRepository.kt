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
import com.veritalex.core.datastore.SavedBooksPreferencesDatastore
import com.veritalex.core.network.api.RetrofitNetworkDataSource
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.withContext
import javax.inject.Inject

/**
 * Repository implementation that uses an offline-first approach.
 * Fetches data from local database first, and then from network if needed.
 *
 * @property network The network data source for fetching books from the server.
 * @property bookDao The DAO for accessing the local books database.
 * @property savedBooksDatastore The datastore for managing saved book IDs.
 */
@OptIn(ExperimentalPagingApi::class, ExperimentalCoroutinesApi::class)
class OfflineFirstBooksRepository
    @Inject
    constructor(
        private val network: RetrofitNetworkDataSource,
        private val bookDao: BookDao,
        private val savedBooksDatastore: SavedBooksPreferencesDatastore,
    ) : BooksRepository {
        override suspend fun saveBook(id: String) {
            savedBooksDatastore.updateBookIds(id)
        }

        override fun fetchRecommendedBooks(topic: String?): Flow<List<Book>> =
            bookDao
                .getRecommendedStream(topic)
                .map { booksEntities ->
                    booksEntities.map { bookEntity ->
                        bookEntity.toBook()
                    }
                }.onEach { books ->
                    if (books.isEmpty()) {
                        withContext(Dispatchers.IO) { getBooks() }
                    }
                }

        override fun fetchBooks(): Flow<PagingData<Book>> =
            Pager(
                config =
                    PagingConfig(
                        pageSize = 50,
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

        override fun fetchSavedBooks(): Flow<List<Book>> =
            savedBooksDatastore.savedBookIds.flatMapLatest { savedBookIds ->
                bookDao.getBookWithIds(savedBookIds.toSet()).flatMapLatest { booksEntities ->
                    val foundBooks = booksEntities.map { it.book.bookId }.toSet()
                    val missingIds = savedBookIds.map { it.toInt() }.toSet() - foundBooks
                    if (missingIds.isNotEmpty()) {
                        getBooks(missingIds)
                    }
                    flowOf(booksEntities.map { it.toBook() })
                }
            }

        /**
         * Fetches books from the network based on the provided IDs and inserts them into the local database.
         *
         * @param ids The set of book IDs to fetch from the network.
         */
        private suspend fun getBooks(ids: Set<Int>? = null) {
            val response =
                network.getBooks(
                    ids = ids,
            )
            if (response.isSuccessful) {
                response.body()?.results?.insertBooks(bookDao)
            }
        }
    }
