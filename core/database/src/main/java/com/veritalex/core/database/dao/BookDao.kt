package com.veritalex.core.database.dao

import androidx.paging.PagingSource
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import com.veritalex.core.database.entities.BookEntity
import com.veritalex.core.database.entities.BookWithPeople
import com.veritalex.core.database.entities.PersonEntity

@Dao
interface BookDao {
    @Transaction
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBookWithPeople(
        book: BookEntity,
        authors: List<PersonEntity>,
        translators: List<PersonEntity>
    )

    @Transaction
    @Query("SELECT * from books")
    fun booksPagingSource(): PagingSource<Int, BookWithPeople>
}