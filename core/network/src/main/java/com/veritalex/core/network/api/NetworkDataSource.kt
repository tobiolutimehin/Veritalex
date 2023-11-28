package com.veritalex.core.network.api

import com.veritalex.core.network.models.BookListResponse
import com.veritalex.core.network.models.NetworkBook
import javax.inject.Inject

interface NetworkDataSource {
    suspend fun getBooks(page: Int? = null): BookListResponse

    suspend fun getBookById(id: Int): NetworkBook
}

class RetrofitNetworkDataSource @Inject constructor(
    private val apiService: GutendexApiService,
) : NetworkDataSource {
    override suspend fun getBooks(page: Int?): BookListResponse = apiService.getBooks(page = page)

    override suspend fun getBookById(id: Int): NetworkBook = apiService.getBookById(id)
}
