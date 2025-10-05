package com.veritalex.core.network.api

import com.veritalex.core.network.models.BookDto
import com.veritalex.core.network.models.BookListResponse
import retrofit2.Response
import javax.inject.Inject

interface NetworkDataSource {
    suspend fun getBooks(
        page: Int? = null,
        ids: Set<Int>? = null,
    ): Response<BookListResponse>

    suspend fun getBookById(id: Int): Response<BookDto>
}

class RetrofitNetworkDataSource
    @Inject
    constructor(
        private val apiService: GutendexApiService,
    ) : NetworkDataSource {
        override suspend fun getBooks(
            page: Int?,
            ids: Set<Int>?,
        ): Response<BookListResponse> = apiService.getBooks(page = page, ids = ids.toString())

        override suspend fun getBookById(id: Int): Response<BookDto> = apiService.getBookById(id)
    }
