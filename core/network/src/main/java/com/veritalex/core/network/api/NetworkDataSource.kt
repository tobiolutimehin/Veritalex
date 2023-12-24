package com.veritalex.core.network.api

import com.veritalex.core.network.models.BookListResponse
import com.veritalex.core.network.models.BookDto
import javax.inject.Inject

interface NetworkDataSource {
    suspend fun getBooks(page: Int? = null): BookListResponse

    suspend fun getBookById(id: Int): BookDto
}

class RetrofitNetworkDataSource @Inject constructor(
    private val apiService: GutendexApiService,
) : NetworkDataSource {
    override suspend fun getBooks(page: Int?): BookListResponse = apiService.getBooks(page = page)

    override suspend fun getBookById(id: Int): BookDto = apiService.getBookById(id)
}
