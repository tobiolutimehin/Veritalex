package com.veritalex.core.database.hilt

import android.content.Context
import androidx.room.Room
import com.veritalex.core.database.VeritalexDatabase
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.database.dao.PersonDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides
    @Singleton
    fun providesNiaDatabase(
        @ApplicationContext context: Context,
    ): VeritalexDatabase = Room.databaseBuilder(
        context,
        VeritalexDatabase::class.java,
        "veritalex-db",
    ).build()

    @Provides
    fun providesBookDao(
        database: VeritalexDatabase
    ): BookDao = database.bookDao()

    @Provides
    fun providesPersonDao(
        database: VeritalexDatabase
    ): PersonDao = database.personDao()
}
