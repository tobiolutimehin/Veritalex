plugins {
    alias(libs.plugins.com.android.application)
    alias(libs.plugins.compose.compiler)
}

android {
    namespace = "com.veritalex"
    compileSdk = 37

    defaultConfig {
        applicationId = "com.veritalex"
        minSdk = 30
        targetSdk = 37
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation(platform(libs.compose.bom))
    implementation(libs.activity.compose)
    implementation(libs.lifecycle.runtime)
    implementation(libs.compose.foundation)
    implementation(libs.material3)
    implementation(libs.ui)
    implementation(project(":feature:books"))
    implementation(project(":core:designsystem"))

    androidTestImplementation(platform(libs.compose.bom))
    androidTestImplementation(libs.androidx.test.ext.junit)
    androidTestImplementation(libs.junit)
    androidTestImplementation(libs.ui.test.junit4)
}
