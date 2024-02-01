package com.veritalex.core.datastore

import android.util.Log
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringSetPreferencesKey
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import java.io.IOException
import javax.inject.Inject

/**
 * Datastore class for managing the saved book IDs using Jetpack DataStore.
 *
 * @property datastore The DataStore instance for storing preferences.
 */
class SavedBooksPreferencesDatastore
    @Inject
    constructor(
        private val datastore: DataStore<Preferences>,
    ) {
        val savedBookIds: Flow<Set<String>> =
            datastore.data
                .map { preferences ->
                    preferences[KEY] ?: emptySet()
                }

        /**
         * Updates the set of saved book IDs based on the provided parameters.
         *
         * @param id The ID of the book to be updated.
         * @param saved `true` if the book is saved, `false` if it is to be removed from saved books.
         *
         * @return [Boolean] if it was successful
         */
        suspend fun updateBookIds(
            id: String,
            saved: Boolean,
        ): Boolean {
            return try {
                datastore.edit { preferences ->
                    val currentBookIds = (preferences[KEY] ?: emptySet()).toMutableSet()
                    if (saved) {
                        currentBookIds.remove(id)
                    } else {
                        currentBookIds.add(id)
                    }
                    preferences[KEY] = currentBookIds
                }
                true
            } catch (ioException: IOException) {
                Log.e(TAG, "Failed to update books", ioException)
                false
            }
        }

        companion object {
            private val KEY = stringSetPreferencesKey("saved_book_ids")
            private const val TAG = "SavedBookPreferencesDatastore"
        }
    }
