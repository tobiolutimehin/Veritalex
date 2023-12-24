package com.veritalex.core.data.repository

import androidx.paging.ExperimentalPagingApi
import androidx.paging.LoadType
import androidx.paging.PagingState
import androidx.paging.RemoteMediator
import com.google.firebase.crashlytics.buildtools.reloc.org.apache.http.HttpException
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.database.entities.BookEntity
import com.veritalex.core.database.entities.BookWithPeople
import com.veritalex.core.database.entities.PersonEntity
import com.veritalex.core.network.api.RetrofitNetworkDataSource
import com.veritalex.core.network.models.BookDto
import com.veritalex.core.network.models.PersonDto
import java.io.IOException
import javax.inject.Inject


@OptIn(ExperimentalPagingApi::class)
class BooksRemoteMediator @Inject constructor(
    private val network: RetrofitNetworkDataSource,
    private val bookDao: BookDao
): RemoteMediator<Int, BookWithPeople>() {
    private var loadKey: Int? = null
    override suspend fun load(
        loadType: LoadType,
        state: PagingState<Int, BookWithPeople>
    ): MediatorResult {
        return try {
            val key = when (loadType) {
                LoadType.REFRESH -> null
                LoadType.PREPEND -> return MediatorResult.Success(endOfPaginationReached = true)
                LoadType.APPEND -> {
                    state.lastItemOrNull()
                        ?: return MediatorResult.Success(
                            endOfPaginationReached = true
                        )

                    loadKey
                }
            }
            val response = network.getBooks(page = key)
            val networkBooks = response.results

            networkBooks.forEach { networkBook ->
                val bookEntity = networkBook.toBookEntity()
                val authors = networkBook.authors.map { it.toPersonEntity() }
                val translators = networkBook.translators?.map { it.toPersonEntity() } ?: emptyList()

                bookDao.insertBookWithPeople(bookEntity, authors, translators)
            }
            loadKey = response.next?.extractPageNumberFromUrl()

            MediatorResult.Success(endOfPaginationReached = (loadKey ?: 0) > 25)
        } catch (e: IOException) {
            MediatorResult.Error(e)
        } catch (e: HttpException) {
            MediatorResult.Error(e)
        }
    }
}

fun PersonDto.toPersonEntity(): PersonEntity {
    return PersonEntity(
        birthYear = this.birthYear,
        deathYear = this.deathYear,
        name = this.name
    )
}

fun BookDto.toBookEntity(): BookEntity {
    return BookEntity(
        bookId = this.id,
        title = this.title,
        subjects = this.subjects,
        bookshelves = this.bookshelves,
        languages = this.languages,
        copyright = this.copyright,
        mediaType = this.mediaType,
        formats = this.formats,
        downloadCount = this.downloadCount
    )
}

fun String.extractPageNumberFromUrl(): Int? {
    val regex = Regex("""[?&]page=(\d+)""")
    val matchResult = regex.find(this)
    return matchResult?.groupValues?.get(1)?.toIntOrNull()
}