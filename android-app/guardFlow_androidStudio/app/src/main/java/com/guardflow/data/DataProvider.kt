package com.guardflow.data

import android.content.Context
import androidx.room.Room
import com.guardflow.data.local.GuardFlowDatabase
import com.guardflow.data.repository.GuardFlowRepository
import com.guardflow.data.repository.GuardFlowRepositoryImpl
import com.guardflow.network.ApiConfig
import com.guardflow.network.GuardFlowApiClient

object DataProvider {
    private var database: GuardFlowDatabase? = null
    private var repository: GuardFlowRepository? = null

    fun provideRepository(context: Context): GuardFlowRepository {
        return repository ?: synchronized(this) {
            val db = database ?: Room.databaseBuilder(
                context.applicationContext,
                GuardFlowDatabase::class.java,
                GuardFlowDatabase.DATABASE_NAME
            ).build().also { database = it }

            val apiClient = GuardFlowApiClient(baseUrl = ApiConfig.BASE_URL)

            GuardFlowRepositoryImpl(db.guardFlowDao(), apiClient).also { repository = it }
        }
    }
}
