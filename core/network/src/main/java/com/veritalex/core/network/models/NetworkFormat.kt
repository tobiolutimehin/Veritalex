package com.veritalex.core.network.models

import kotlinx.serialization.Serializable

/**
 * Network format from the Gutendex API.
 *
 * @property formats The formats of the book.
 */
@Serializable
data class NetworkFormat(
    val formats: Map<String, String>,
)
