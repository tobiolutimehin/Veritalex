plugins {
    alias(libs.plugins.com.android.application)
    alias(libs.plugins.org.jetbrains.kotlin.android)
    alias(libs.plugins.gms.google.services)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
}

android {
    namespace = "com.veritalex"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.veritalex"
        minSdk = 30
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.15"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(libs.activity.compose)
    implementation(libs.core.ktx)
    implementation(libs.core.splashscreen)
    implementation(libs.material3)
    implementation(libs.lifecycle.runtime.ktx)
    implementation(libs.ui)
    implementation(libs.ui.graphics)
    implementation(libs.ui.tooling.preview)
    implementation(platform(libs.compose.bom))
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)

    testImplementation(libs.junit)

    androidTestImplementation(libs.androidx.test.ext.junit)
    androidTestImplementation(libs.espresso.core)
    androidTestImplementation(libs.ui.test.junit4)
    androidTestImplementation(platform(libs.compose.bom))

    debugImplementation(libs.ui.tooling)
    debugImplementation(libs.ui.test.manifest)

    implementation(libs.lifecycle.viewmodel.compose)
    implementation(libs.material3.adaptive.navigation.suite)
    implementation(libs.material3.windowSizeClass)
    implementation(libs.material3.adaptive)

    // Firebase
    implementation(platform(libs.firebase.bom))
    implementation(libs.firebase.analytics)

    implementation(libs.androidx.paging.runtime.ktx)
    implementation(libs.androidx.paging.compose)

    // Retrofit
    implementation(libs.jakewharton.serialization.converter)
    implementation(libs.retrofit)
    implementation(libs.squareup.okhttp3)
    implementation(libs.coil.compose)
    implementation(libs.androidx.navigation.compose)

    // Modules
    implementation(project(mapOf("path" to ":core:network")))
    implementation(project(mapOf("path" to ":core:data")))
    implementation(project(mapOf("path" to ":core:designsystem")))
    implementation(project(mapOf("path" to ":feature:home")))
}
