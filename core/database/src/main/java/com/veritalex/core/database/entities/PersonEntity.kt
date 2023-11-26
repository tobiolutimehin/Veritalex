package com.veritalex.core.database.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "persons")
data class PersonEntity(
    @PrimaryKey(autoGenerate = true)
    val personId: Long = 0,
    val birthYear: Int?,
    val deathYear: Int?,
    val name: String,
)
