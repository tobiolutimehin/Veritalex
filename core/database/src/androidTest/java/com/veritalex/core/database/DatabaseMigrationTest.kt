package com.veritalex.core.database

import androidx.room.testing.MigrationTestHelper
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class DatabaseMigrationTest {
    @get:Rule
    val helper = MigrationTestHelper(InstrumentationRegistry.getInstrumentation(), VeritalexDatabase::class.java)

    @Test
    fun migrationPreservesCachedBooksAndPeople() {
        helper.createDatabase("migration-test", 1).use { database ->
            database.execSQL("INSERT INTO books VALUES (1342, 'Pride and Prejudice', '[]', '[]', '[\"en\"]', 0, 'Text', 0, '{}')")
            database.execSQL("INSERT INTO persons VALUES (1, 1775, 1817, 'Jane Austen')")
        }
        helper.runMigrationsAndValidate("migration-test", 2, true, MIGRATION_1_2).use { database ->
            database.query("SELECT title FROM books WHERE bookId = 1342").use {
                it.moveToFirst()
                assertEquals("Pride and Prejudice", it.getString(0))
            }
            database.query("SELECT name FROM persons WHERE personId = 1").use {
                it.moveToFirst()
                assertEquals("Jane Austen", it.getString(0))
            }
            // Old rows never contained reliable membership, so do not invent it.
            database.query("SELECT COUNT(*) FROM book_authors").use {
                it.moveToFirst()
                assertEquals(0, it.getInt(0))
            }
        }
    }
}
