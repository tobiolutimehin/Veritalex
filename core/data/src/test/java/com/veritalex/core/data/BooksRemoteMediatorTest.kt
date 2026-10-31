package com.veritalex.core.data

import androidx.paging.ExperimentalPagingApi
import androidx.paging.LoadType
import androidx.paging.PagingConfig
import androidx.paging.PagingSource
import androidx.paging.PagingState
import androidx.paging.RemoteMediator.MediatorResult
import com.veritalex.core.data.repository.BooksRemoteMediator
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.database.entities.BookEntity
import com.veritalex.core.database.entities.BookAuthorCrossRef
import com.veritalex.core.database.entities.BookTranslatorCrossRef
import com.veritalex.core.database.entities.BookWithPeople
import com.veritalex.core.database.entities.PersonEntity
import com.veritalex.core.network.api.GutendexApiService
import com.veritalex.core.network.api.RetrofitNetworkDataSource
import com.veritalex.core.network.models.BookDto
import com.veritalex.core.network.models.BookListResponse
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.runBlocking
import okhttp3.ResponseBody.Companion.toResponseBody
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import retrofit2.Response

@OptIn(ExperimentalPagingApi::class)
class BooksRemoteMediatorTest {
    private val state = PagingState<Int, BookWithPeople>(emptyList(), null, PagingConfig(32), 0)

    private fun mediator(response: Response<BookListResponse>): BooksRemoteMediator {
        val api = object : GutendexApiService {
            override suspend fun getBooks(
                authorYearStart: Int?, authorYearEnd: Int?, copyright: String?, ids: String?,
                languages: String?, mimeType: String?, search: String?, sort: String?, topic: String?, page: Int?,
            ) = response
            override suspend fun getBookById(id: Int): Response<BookDto> = error("Unused")
        }
        val dao = object : BookDao {
            override suspend fun upsertBook(book: BookEntity) = Unit
            override suspend fun insertPerson(person: PersonEntity): Long = error("Unused")
            override suspend fun findPersonId(name: String, birthYear: Int?, deathYear: Int?): Long? = error("Unused")
            override suspend fun insertAuthor(crossRef: BookAuthorCrossRef) = Unit
            override suspend fun insertTranslator(crossRef: BookTranslatorCrossRef) = Unit
            override suspend fun clearAuthors(bookId: Int) = Unit
            override suspend fun clearTranslators(bookId: Int) = Unit
            override suspend fun insertBookWithPeople(book: BookEntity, authors: List<PersonEntity>, translators: List<PersonEntity>) = Unit
            override fun booksPagingSource(): PagingSource<Int, BookWithPeople> = error("Unused")
            override fun getRecommendedStream(topic: String?): Flow<List<BookWithPeople>> = flowOf(emptyList())
            override fun getBookWithIds(ids: Set<String>): Flow<List<BookWithPeople>> = flowOf(emptyList())
        }
        return BooksRemoteMediator(RetrofitNetworkDataSource(api), dao)
    }

    @Test
    fun lastPageEndsPagination() = runBlocking {
        val result = mediator(Response.success(BookListResponse(0, null, null, emptyList())))
            .load(LoadType.REFRESH, state) as MediatorResult.Success
        assertTrue(result.endOfPaginationReached)
    }

    @Test
    fun nextPageBeyondTwentyFiveIsStillAvailable() = runBlocking {
        val result = mediator(Response.success(BookListResponse(1000, "https://gutendex.com/books/?page=26", null, emptyList())))
            .load(LoadType.REFRESH, state) as MediatorResult.Success
        assertFalse(result.endOfPaginationReached)
    }

    @Test
    fun httpFailureCanBeRetried() = runBlocking {
        val result = mediator(Response.error(503, "unavailable".toResponseBody()))
            .load(LoadType.REFRESH, state)
        assertTrue(result is MediatorResult.Error)
    }

    @Test
    fun missingBodyIsAnError() = runBlocking {
        val result = mediator(Response.success(null)).load(LoadType.REFRESH, state)
        assertTrue(result is MediatorResult.Error)
    }
}
