package com.veritalex.core.database

import androidx.room.Database
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase
import com.veritalex.core.database.entities.BookAuthorCrossRef
import com.veritalex.core.database.entities.BookTranslatorCrossRef
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.database.dao.PersonDao
import com.veritalex.core.database.entities.BookEntity
import com.veritalex.core.database.entities.PersonEntity
import com.veritalex.core.database.util.VeritalexTypeConverters

@Database(
    entities = [PersonEntity::class, BookEntity::class, BookAuthorCrossRef::class, BookTranslatorCrossRef::class],
    version = 2,
    exportSchema = true
)
@TypeConverters(VeritalexTypeConverters::class)
abstract class VeritalexDatabase: RoomDatabase() {
    abstract fun bookDao(): BookDao

    abstract fun personDao(): PersonDao
}

// Version 1 stored people without book membership; keep all existing rows.
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        for (table in listOf("book_authors", "book_translators")) {
            db.execSQL("CREATE TABLE IF NOT EXISTS `$table` (`bookId` INTEGER NOT NULL, `personId` INTEGER NOT NULL, PRIMARY KEY(`bookId`, `personId`), FOREIGN KEY(`bookId`) REFERENCES `books`(`bookId`) ON UPDATE NO ACTION ON DELETE CASCADE, FOREIGN KEY(`personId`) REFERENCES `persons`(`personId`) ON UPDATE NO ACTION ON DELETE CASCADE)")
            db.execSQL("CREATE INDEX IF NOT EXISTS `index_${table}_personId` ON `$table` (`personId`)")
        }
    }
}
