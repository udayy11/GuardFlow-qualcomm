package com.guardflow.network

import com.guardflow.model.GuardFlowEvent
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

class GuardFlowApiClient(
    private val baseUrl: String,
    private val client: OkHttpClient = OkHttpClient()
) {
    private val jsonMediaType = "application/json; charset=utf-8".toMediaType()

//    fun sendEvent(event: GuardFlowEvent): Boolean {
//        val body = JSONObject(event.toWireJson()).toString().toRequestBody(jsonMediaType)
//        val request = Request.Builder()
//            .url("$baseUrl/events")
//            .post(body)
//            .build()
//
//        return try {
//            client.newCall(request).execute().use { response ->
//                response.isSuccessful
//            }
//        } catch (e: Exception) {
//            false
//        }
//    }
        fun sendEvent(event: GuardFlowEvent): Boolean {
            val body = JSONObject(event.toWireJson())
                .toString()
                .toRequestBody(jsonMediaType)

            val request = Request.Builder()
                .url("$baseUrl/events")
                .post(body)
                .build()

            try {
                client.newCall(request).execute().use { response ->

                    android.util.Log.d(
                        "GuardFlowNetwork",
                        "POST ${request.url} -> ${response.code}"
                    )

                    val responseBody = response.body?.string()

                    android.util.Log.d(
                        "GuardFlowNetwork",
                        "Response: $responseBody"
                    )

                    return response.isSuccessful
                }

            } catch (e: Exception) {

                android.util.Log.e(
                    "GuardFlowNetwork",
                    "Network Error",
                    e
                )

                return false
            }
        }

    fun fetchRiskScore(sessionId: String): String? {
        val body = "".toRequestBody(jsonMediaType)
        val request = Request.Builder()
            .url("$baseUrl/score/$sessionId")
            .post(body)
            .build()

        return try {
            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    response.body?.string()
                } else {
                    null
                }
            }
        } catch (e: Exception) {
            null
        }
    }
}
