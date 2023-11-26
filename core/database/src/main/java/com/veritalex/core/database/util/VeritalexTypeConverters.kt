package com.veritalex.core.database.util

import androidx.room.TypeConverter
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

class VeritalexTypeConverters {
    private val gson = Gson()
    @TypeConverter
    fun stringToMapOfStrings(value: String): Map<String, String> {
        val mapType = object : TypeToken<Map<String, String>>() {}.type
        return gson.fromJson(value, mapType)
    }

    @TypeConverter
    fun mapOfStringsToString(map: Map<String, String>): String {
        return gson.toJson(map)
    }


    @TypeConverter
    fun stringToListOfString(value: String?): List<String> {
        if (value.isNullOrEmpty()) return emptyList()

        val listType = object : TypeToken<List<String>>() {}.type
        return gson.fromJson(value, listType)
    }

    @TypeConverter
    fun listOStringToString(list: List<String>?): String {
        return gson.toJson(list ?: emptyList<String>())
    }
}
