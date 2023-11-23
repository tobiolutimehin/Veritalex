package com.veritalex.core.network.api

import com.veritalex.core.network.models.BookListResponse
import com.veritalex.core.network.models.NetworkBook
import javax.inject.Inject

interface NetworkDataSource {
    suspend fun getBooks(): BookListResponse

    suspend fun getBookById(id: Int): NetworkBook
}

class RetrofitNetworkDataSource @Inject constructor(
    private val apiService: GutendexApiService,
) : NetworkDataSource {
    override suspend fun getBooks(): BookListResponse = apiService.getBooks()

    override suspend fun getBookById(id: Int): NetworkBook = apiService.getBookById(id)
}
