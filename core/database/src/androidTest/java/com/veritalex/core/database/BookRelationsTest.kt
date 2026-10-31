package com.veritalex.core.database

import android.content.Context
import androidx.room.Room
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.veritalex.core.database.entities.BookEntity
import com.veritalex.core.database.entities.PersonEntity
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class BookRelationsTest {
    @Test
    fun authorsAndTranslatorsRoundTripWithoutDuplicates() = runBlocking {
        val context = ApplicationProvider.getApplicationContext<Context>()
        val database = Room.inMemoryDatabaseBuilder(context, VeritalexDatabase::class.java).build()
        try {
            val book = BookEntity(1342, "Pride and Prejudice", emptyList(), emptyList(), listOf("en"), false, "Text", 0, emptyMap())
            val author = PersonEntity(name = "Jane Austen", birthYear = 1775, deathYear = 1817)
            val translator = PersonEntity(name = "Translator", birthYear = null, deathYear = null)
            repeat(2) { database.bookDao().insertBookWithPeople(book, listOf(author), listOf(translator)) }
            val saved = database.bookDao().getBookWithIds(setOf("1342")).first().single()
            assertEquals(listOf("Jane Austen"), saved.authors.map { it.name })
            assertEquals(listOf("Translator"), saved.translators.map { it.name })
            database.openHelper.readableDatabase.query("SELECT COUNT(*) FROM persons").use {
                it.moveToFirst()
                assertEquals(2, it.getInt(0))
            }
        } finally {
            database.close()
        }
    }
}
