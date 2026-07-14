package com.guardflow.model

import java.util.Locale

enum class EventType {
    APP_OPENED,
    WEBSITE_OPENED,
    FORM_FIELD_FILLED,
    FORM_SUBMITTED,
    SMS_RECEIVED,
    LINK_CLICKED,
    CONTACT_ADDED,
    CALL_STARTED,
    SCREEN_SHARE_STARTED,
    PAYMENT_APP_OPENED,
    PAYMENT_INITIATED,
    PAYMENT_CONFIRMED;

    fun wireValue(): String {
        return name.lowercase(Locale.ROOT)
    }
}
