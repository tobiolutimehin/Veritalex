package com.veritalex.core.data.di

import com.veritalex.core.data.repository.BooksRepository
import com.veritalex.core.data.repository.OfflineFirstBooksRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent

@Module
@InstallIn(SingletonComponent::class)
interface RepositoryModule {
    @Binds
    fun bindsBooksRepository(
        booksRepository: OfflineFirstBooksRepository,
    ): BooksRepository
}
