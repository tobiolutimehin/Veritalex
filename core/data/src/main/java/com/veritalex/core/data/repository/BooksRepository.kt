package com.veritalex.core.data.repository

import androidx.paging.PagingData
import com.veritalex.core.data.models.Book
import kotlinx.coroutines.flow.Flow

/**
 * Interface defining the contract for a BooksRepository.
 * Provides methods to fetch books, fetch recommended books, save a book, and fetch saved books.
 */
interface BooksRepository {
    /**
     * Fetches a paginated list of books.
     *
     * @return A [Flow] emitting [PagingData] containing [Book] objects.
     */
    fun fetchBooks(): Flow<PagingData<Book>>

    /**
     * Fetches a list of recommended books based on the given topic.
     *
     * @param topic The topic to filter recommended books by. If null, fetches general recommendations.
     * @return A [Flow] emitting a list of [Book] objects.
     */
    fun fetchRecommendedBooks(topic: String? = null): Flow<List<Book>>

    /**
     * Saves a book by its ID.
     *
     * @param id The ID of the book to save.
     */
    suspend fun saveBook(id: String)

    /**
     * Fetches a list of saved books.
     *
     * @return A [Flow] emitting a list of [Book] objects.
     */
    fun fetchSavedBooks(): Flow<List<Book>>
}
