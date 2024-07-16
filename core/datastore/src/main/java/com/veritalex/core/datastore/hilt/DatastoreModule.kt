package com.veritalex.core.datastore.hilt

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import com.veritalex.core.datastore.SavedBooksPreferencesDatastore
import com.veritalex.core.datastore.utils.Constants.SAVED_BOOK_IDS_KEY
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatastoreModule {
    private const val USER_PREFERENCES_NAME = SAVED_BOOK_IDS_KEY

    private val Context.dataStore by preferencesDataStore(
        name = USER_PREFERENCES_NAME,
    )

    @Provides
    @Singleton
    fun provideDataStore(
        @ApplicationContext context: Context,
    ): DataStore<Preferences> = context.dataStore

    @Provides
    @Singleton
    fun provideSavedBooksPreferencesDatastore(dataStore: DataStore<Preferences>): SavedBooksPreferencesDatastore =
        SavedBooksPreferencesDatastore(dataStore)
}
