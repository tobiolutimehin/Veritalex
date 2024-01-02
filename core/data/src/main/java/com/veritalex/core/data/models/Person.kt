package com.veritalex.core.data.models

/**
 * Represents information about a person.
 *
 * @property birthYear The birth year of the person. Can be null if unknown.
 * @property deathYear The death year of the person. Can be null if still alive or unknown.
 * @property name The name of the person.
 */
data class Person(
    val birthYear: Int?,
    val deathYear: Int?,
    val name: String,
)
