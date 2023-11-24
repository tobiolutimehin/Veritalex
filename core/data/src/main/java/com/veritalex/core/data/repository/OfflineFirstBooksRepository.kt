package com.veritalex.core.data.repository

import com.veritalex.core.network.api.RetrofitNetworkDataSource
import com.veritalex.core.network.models.BookListResponse
import javax.inject.Inject

interface BooksRepository {
    suspend fun fetchBooks(): BookListResponse

    fun fetchBookById(id: Int)
}

class OfflineFirstBooksRepository @Inject constructor(
    private val network: RetrofitNetworkDataSource,
) : BooksRepository {

    override fun fetchBookById(id: Int) {
        TODO("Not yet implemented")
    }

    override suspend fun fetchBooks() =
        network.getBooks()
}
