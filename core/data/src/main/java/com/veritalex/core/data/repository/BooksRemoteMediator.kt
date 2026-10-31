package com.veritalex.core.data.repository

import androidx.paging.ExperimentalPagingApi
import androidx.paging.LoadType
import androidx.paging.PagingState
import androidx.paging.RemoteMediator
import com.veritalex.core.data.utils.Extensions.insertBooks
import com.veritalex.core.data.utils.StringExtensions.extractPageNumberFromUrl
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.database.entities.BookWithPeople
import com.veritalex.core.network.api.RetrofitNetworkDataSource
import retrofit2.HttpException
import kotlinx.serialization.SerializationException
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
                        LoadType.APPEND -> loadKey
                            ?: return MediatorResult.Success(endOfPaginationReached = true)
                    }
                val response = network.getBooks(page = key)

                if (!response.isSuccessful) throw HttpException(response)
                val body = response.body() ?: throw IOException("Empty catalogue response")
                val nextKey = body.next?.let {
                    it.extractPageNumberFromUrl() ?: throw IOException("Invalid catalogue page")
                }
                body.results.insertBooks(bookDao)
                loadKey = nextKey
                MediatorResult.Success(endOfPaginationReached = body.next == null)
            } catch (e: IOException) {
                MediatorResult.Error(e)
            } catch (e: HttpException) {
                MediatorResult.Error(e)
            } catch (e: SerializationException) {
                MediatorResult.Error(e)
            }
        }
    }
