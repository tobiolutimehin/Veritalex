package com.veritalex.core.data.repository

import androidx.paging.ExperimentalPagingApi
import androidx.paging.LoadType
import androidx.paging.PagingState
import androidx.paging.RemoteMediator
import com.google.firebase.crashlytics.buildtools.reloc.org.apache.http.HttpException
import com.veritalex.core.data.utils.Extensions.insertBooks
import com.veritalex.core.data.utils.StringExtensions.extractPageNumberFromUrl
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.database.entities.BookWithPeople
import com.veritalex.core.network.api.RetrofitNetworkDataSource
import java.io.IOException
import javax.inject.Inject

@OptIn(ExperimentalPagingApi::class)
class BooksRemoteMediator
    @Inject
    constructor(
        private val network: RetrofitNetworkDataSource,
        private val bookDao: BookDao,
    ) : RemoteMediator<Int, BookWithPeople>() {
        private var loadKey: Int? = null

        override suspend fun load(
            loadType: LoadType,
            state: PagingState<Int, BookWithPeople>,
        ): MediatorResult {
            return try {
                val key =
                    when (loadType) {
                        LoadType.REFRESH -> null
                        LoadType.PREPEND -> return MediatorResult.Success(endOfPaginationReached = true)
                        LoadType.APPEND -> {
                            state.lastItemOrNull()
                                ?: return MediatorResult.Success(
                                    endOfPaginationReached = true,
                                )

                            loadKey
                        }
                    }
                val response = network.getBooks(page = key)

                if (response.isSuccessful) {
                    response.body()?.let { body ->
                        val networkBooks = body.results
                        networkBooks.insertBooks(bookDao)
                        loadKey = body.next?.extractPageNumberFromUrl()
                    }
                }

                MediatorResult.Success(endOfPaginationReached = (loadKey ?: 0) > 25)
            } catch (e: IOException) {
                MediatorResult.Error(e)
            } catch (e: HttpException) {
                MediatorResult.Error(e)
            }
        }
    }
