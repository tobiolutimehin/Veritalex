package com.veritalex.core.database.dao

import androidx.paging.PagingSource
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import androidx.room.Upsert
import com.veritalex.core.database.entities.BookAuthorCrossRef
import com.veritalex.core.database.entities.BookTranslatorCrossRef
import com.veritalex.core.database.entities.BookEntity
import com.veritalex.core.database.entities.BookWithPeople
import com.veritalex.core.database.entities.PersonEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface BookDao {
    @Transaction
    suspend fun insertBookWithPeople(
        book: BookEntity,
        authors: List<PersonEntity>,
        translators: List<PersonEntity>,
    ) {
        upsertBook(book)
        clearAuthors(book.bookId)
        clearTranslators(book.bookId)
        for (author in authors) insertAuthor(BookAuthorCrossRef(book.bookId, findOrInsertPerson(author)))
        for (translator in translators) insertTranslator(BookTranslatorCrossRef(book.bookId, findOrInsertPerson(translator)))
    }

    private suspend fun findOrInsertPerson(person: PersonEntity): Long =
        findPersonId(person.name, person.birthYear, person.deathYear) ?: insertPerson(person)

    @Upsert
    suspend fun upsertBook(book: BookEntity)

    @Insert
    suspend fun insertPerson(person: PersonEntity): Long

    @Query("SELECT personId FROM persons WHERE name = :name AND birthYear IS :birthYear AND deathYear IS :deathYear LIMIT 1")
    suspend fun findPersonId(name: String, birthYear: Int?, deathYear: Int?): Long?

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertAuthor(crossRef: BookAuthorCrossRef)

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertTranslator(crossRef: BookTranslatorCrossRef)

    @Query("DELETE FROM book_authors WHERE bookId = :bookId")
    suspend fun clearAuthors(bookId: Int)

    @Query("DELETE FROM book_translators WHERE bookId = :bookId")
    suspend fun clearTranslators(bookId: Int)

    @Transaction
    @Query("SELECT * from books")
    fun booksPagingSource(): PagingSource<Int, BookWithPeople>

    @Transaction
    @Query("SELECT * FROM books WHERE (:topic IS NULL OR :topic = '' OR :topic IN (subjects)) OR COALESCE(:topic, '') = ''")
    fun getRecommendedStream(topic: String?): Flow<List<BookWithPeople>>

    @Transaction
    @Query("SELECT * FROM books WHERE bookId IN (:ids)")
    fun getBookWithIds(ids: Set<String>): Flow<List<BookWithPeople>>
}
