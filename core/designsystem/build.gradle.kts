plugins {
    alias(libs.plugins.com.android.library)
    alias(libs.plugins.compose.compiler)
}

android {
    namespace = "com.veritalex.core.designsystem"
    compileSdk = 37

    defaultConfig {
        minSdk = 30
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
    implementation(libs.lifecycle.runtime)
    implementation(libs.compose.foundation)
    implementation(libs.material3)
    implementation(libs.ui)
}
