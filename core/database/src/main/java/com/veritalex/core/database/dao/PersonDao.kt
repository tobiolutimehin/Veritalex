package com.veritalex.core.database.dao

import androidx.room.Dao
import androidx.room.Query
import com.veritalex.core.database.entities.PersonEntity

@Dao
interface PersonDao {
    @Query(
        "SELECT * FROM persons " +
                "WHERE name = :name AND birthYear = :birthYear AND deathYear = :deathYear"
    )
    suspend fun getPersonByNameBirthAndDeath(
        name: String,
        birthYear: Int?,
        deathYear: Int?
    ): PersonEntity?
}