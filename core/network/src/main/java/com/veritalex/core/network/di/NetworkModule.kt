package com.veritalex.core.network.di

import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import com.veritalex.core.network.api.GutendexApiService
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import retrofit2.Retrofit
import java.net.URL
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Singleton
    @Provides
    fun provideBaseUrl(): URL = URL("https://gutendex.com/")

    @Singleton
    @Provides
    fun provideJson(): Json =
        Json {
            ignoreUnknownKeys = true
            isLenient = true
            prettyPrint = true
            encodeDefaults = true
        }

    @Singleton
    @Provides
    fun provideRetrofit(
        json: Json,
        base: URL,
    ): Retrofit =
        Retrofit
            .Builder()
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .baseUrl(base)
            .build()

    @Singleton
    @Provides
    fun provideRetrofitService(retrofit: Retrofit): GutendexApiService = retrofit.create(GutendexApiService::class.java)
}
