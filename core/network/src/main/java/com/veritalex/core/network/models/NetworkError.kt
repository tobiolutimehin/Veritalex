package com.veritalex.core.network.models

import kotlinx.serialization.Serializable

/**
 * A network error from the Gutendex API.
 *
 * @property detail The detail of the error.
 */
@Serializable
data class NetworkError(
    val detail: String,
)
