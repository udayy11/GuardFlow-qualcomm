package com.guardflow.model

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.time.Instant
import java.time.format.DateTimeFormatter
import java.util.UUID

@Entity(tableName = "events")
data class GuardFlowEvent(
    @PrimaryKey val eventId: String = UUID.randomUUID().toString(),
    val sessionId: String,
    val eventType: EventType,
    val timestamp: Instant = Instant.now(),
    val sourceApp: String? = null,
    val metadata: Map<String, Any?> = emptyMap()
) {
    fun toWireJson(): Map<String, Any?> {
        return mapOf(
            "event_id" to eventId,
            "session_id" to sessionId,
            "event_type" to eventType.wireValue(),
            "timestamp" to DateTimeFormatter.ISO_INSTANT.format(timestamp),
            "source_app" to sourceApp,
            "payload" to metadata
        )
    }
}
