package com.veritalex.core.database

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.veritalex.core.database.dao.BookDao
import com.veritalex.core.database.dao.PersonDao
import com.veritalex.core.database.entities.BookEntity
import com.veritalex.core.database.entities.PersonEntity
import com.veritalex.core.database.util.VeritalexTypeConverters

@Database(
    entities = [PersonEntity::class, BookEntity::class],
    version = 1,
    exportSchema = false
)
@TypeConverters(VeritalexTypeConverters::class)
abstract class VeritalexDatabase: RoomDatabase() {
    abstract fun bookDao(): BookDao

    abstract fun personDao(): PersonDao
}
