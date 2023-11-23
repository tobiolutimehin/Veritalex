package com.veritalex.core.data.repository

import com.veritalex.core.network.api.RetrofitNetworkDataSource
import javax.inject.Inject

interface BooksRepository

class OfflineFirstBooksRepository @Inject constructor(
    private val network: RetrofitNetworkDataSource,
) : BooksRepository
