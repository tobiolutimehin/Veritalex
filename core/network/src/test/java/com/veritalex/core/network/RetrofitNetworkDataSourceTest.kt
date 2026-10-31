package com.veritalex.core.network

import com.veritalex.core.network.api.GutendexApiService
import com.veritalex.core.network.api.RetrofitNetworkDataSource
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import mockwebserver3.MockResponse
import mockwebserver3.MockWebServer
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Before
import org.junit.Test
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory

class RetrofitNetworkDataSourceTest {
    private val server = MockWebServer()
    private lateinit var source: RetrofitNetworkDataSource

    @Before
    fun setUp() {
        server.start()
        source = RetrofitNetworkDataSource(
            Retrofit.Builder().baseUrl(server.url("/"))
                .addConverterFactory(Json.asConverterFactory("application/json".toMediaType()))
                .build().create(GutendexApiService::class.java),
        )
        server.enqueue(MockResponse.Builder().body("""{"count":0,"next":null,"previous":null,"results":[]}""").build())
    }

    @After
    fun tearDown() { server.close() }

    @Test
    fun catalogueRequestOmitsAbsentIds() = runBlocking {
        source.getBooks(page = 2, ids = null)
        val url = server.takeRequest().url
        assertNull(url.queryParameter("ids"))
        assertEquals("2", url.queryParameter("page"))
    }

    @Test
    fun requestedIdsAreCommaSeparated() = runBlocking {
        source.getBooks(page = null, ids = linkedSetOf(84, 1342))
        assertEquals("84,1342", server.takeRequest().url.queryParameter("ids"))
    }
}
