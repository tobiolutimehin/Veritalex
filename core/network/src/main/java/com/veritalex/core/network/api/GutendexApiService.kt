package com.veritalex.core.network.api

import com.veritalex.core.network.models.BookListResponse
import com.veritalex.core.network.models.NetworkBook
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface GutendexApiService {
    @GET("books")
    suspend fun getBooks(
        @Query("author_year_start") authorYearStart: Int? = null,
        @Query("author_year_end") authorYearEnd: Int? = null,
        @Query("copyright") copyright: String? = null,
        @Query("ids") ids: String? = null,
        @Query("languages") languages: String? = null,
        @Query("mime_type") mimeType: String? = null,
        @Query("search") search: String? = null,
        @Query("sort") sort: String? = null,
        @Query("topic") topic: String? = null,
        @Query("page") page: Int? = null,
    ): BookListResponse

    @GET("books/{id}")
    fun getBookById(@Path("id") id: Int): NetworkBook
}
