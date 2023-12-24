package com.veritalex.core.network.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * A person from the Gutendex API.
 *
 * @property birthYear The birth year of the person.
 * @property deathYear The death year of the person.
 * @property name The name of the person.
 */
@Serializable
data class PersonDto(
    @SerialName("birth_year")
    val birthYear: Int? = null,
    @SerialName("death_year")
    val deathYear: Int? = null,
    val name: String,
)
