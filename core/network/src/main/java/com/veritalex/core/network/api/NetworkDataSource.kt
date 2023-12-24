package com.veritalex.core.network.api

import com.veritalex.core.network.models.BookListResponse
import com.veritalex.core.network.models.BookDto
import retrofit2.Response
import javax.inject.Inject

interface NetworkDataSource {
    suspend fun getBooks(page: Int? = null): Response<BookListResponse>

    suspend fun getBookById(id: Int): Response<BookDto>
}

class RetrofitNetworkDataSource @Inject constructor(
    private val apiService: GutendexApiService,
) : NetworkDataSource {
    override suspend fun getBooks(page: Int?): Response<BookListResponse> = apiService.getBooks(page = page)

    override suspend fun getBookById(id: Int): Response<BookDto> = apiService.getBookById(id)
}
