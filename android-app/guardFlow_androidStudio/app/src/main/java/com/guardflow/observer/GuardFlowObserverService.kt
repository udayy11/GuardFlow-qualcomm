package com.guardflow.observer

import android.accessibilityservice.AccessibilityService
import android.util.Log
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import com.guardflow.data.DataProvider
import com.guardflow.data.SessionManager
import com.guardflow.data.repository.GuardFlowRepository
import com.guardflow.model.EventType
import com.guardflow.model.GuardFlowEvent
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

class GuardFlowObserverService : AccessibilityService() {

    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private lateinit var repository: GuardFlowRepository
    private lateinit var sessionId: String
    
    private var lastRecordedUrl: String? = null
    private var lastRecordedApp: String? = null

    override fun onServiceConnected() {
        super.onServiceConnected()
        repository = DataProvider.provideRepository(this)
        val sessionManager = SessionManager(this)
        sessionId = runBlocking { sessionManager.getOrCreateSessionId() }
        Log.d("GuardFlowObserver", "Service Connected - Session: $sessionId")
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event == null) return
        
        val pkg = event.packageName?.toString() ?: ""

        when (event.eventType) {
            AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED -> {
                if (pkg != this.packageName) {
                    recordAppOpened(pkg)
                }
            }
            AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED,
            AccessibilityEvent.TYPE_VIEW_SCROLLED,
            AccessibilityEvent.TYPE_VIEW_FOCUSED -> {
                if (pkg.contains("chrome") || pkg.contains("browser") || pkg.contains("sbrowser")) {
                    scanForBrowserUrl(pkg)
                }
            }
            AccessibilityEvent.TYPE_VIEW_CLICKED -> {
                val source = event.source
                if (source != null) {
                    checkForLinkClicked(source, pkg)
                }
            }
        }
    }

    private fun scanForBrowserUrl(packageName: String) {
        val root = rootInActiveWindow ?: return
        
        // Known Browser URL Bar IDs
        val urlBarIds = listOf(
            "com.android.chrome:id/url_bar",
            "com.sec.android.app.sbrowser:id/location_bar_edit_text",
            "org.mozilla.firefox:id/url_bar_title"
        )
        
        for (id in urlBarIds) {
            val nodes = root.findAccessibilityNodeInfosByViewId(id)
            if (nodes.isNotEmpty()) {
                val url = nodes[0].text?.toString()
                if (!url.isNullOrBlank() && (url.contains(".") || url.contains("http"))) {
                    recordLinkClicked(url, packageName)
                    return // Found it
                }
            }
        }
        
        // Fallback to recursive scan if ID search fails
        findUrlInNodeTree(root, packageName)
    }

    private fun recordAppOpened(packageName: String) {
        if (packageName == lastRecordedApp) return
        lastRecordedApp = packageName

        serviceScope.launch {
            val event = GuardFlowEvent(
                sessionId = sessionId,
                eventType = EventType.APP_OPENED,
                sourceApp = packageName,
                metadata = mapOf("package_name" to packageName)
            )
            repository.recordEvent(event)
            Log.d("GuardFlowObserver", "Recorded App Opened: $packageName")
        }
    }

    private fun checkForLinkClicked(node: AccessibilityNodeInfo, packageName: String?) {
        // Search the node and its children for anything that looks like a URL
        val text = node.text?.toString() ?: ""
        val contentDesc = node.contentDescription?.toString() ?: ""
        
        val urlPattern = Regex("(?i)\\b((?:https?://|www\\d{0,3}[.]|[a-z0-9.\\-]+[.][a-z]{2,4}/)(?:[^\\s()<>]+|\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\))+(?:\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\)|[^\\s`!()\\[\\]{};:'\".,<>?«»“”‘’]))")
        
        val match = urlPattern.find(text) ?: urlPattern.find(contentDesc)
        
        if (match != null) {
            recordLinkClicked(match.value, packageName)
        } else {
            // If the node itself doesn't have a URL, check if it's a browser URL bar 
            // often found in Chrome/Browsers
            if (packageName?.contains("chrome") == true || packageName?.contains("browser") == true) {
                // Browsers often put the URL in a specific view. 
                // As a fallback, we can scan the whole window for URL-like strings
                rootInActiveWindow?.let { root ->
                    findUrlInNodeTree(root, packageName)
                }
            }
        }
    }

    private fun findUrlInNodeTree(node: AccessibilityNodeInfo, packageName: String?) {
        val text = node.text?.toString() ?: ""
        val contentDesc = node.contentDescription?.toString() ?: ""
        val className = node.className?.toString() ?: ""
        
        // Browsers like Chrome use android.widget.EditText or View for the URL bar
        // We look for anything that looks like a URL
        val potentialUrl = if (text.contains(".") && !text.contains(" ")) text else if (contentDesc.contains(".") && !contentDesc.contains(" ")) contentDesc else null

        if (potentialUrl != null && potentialUrl.length > 4 && !potentialUrl.contains(this.packageName)) {
             Log.d("GuardFlowObserver", "Found potential URL in tree: $potentialUrl")
             recordLinkClicked(potentialUrl, packageName)
             // Don't return here, keep scanning to find the most specific one, 
             // but recordLinkClicked handles deduplication
        }

        for (i in 0 until node.childCount) {
            node.getChild(i)?.let { findUrlInNodeTree(it, packageName) }
        }
    }

    private fun recordLinkClicked(url: String, sourceApp: String?) {
        if (url == lastRecordedUrl) return // Skip identical consecutive URLs
        lastRecordedUrl = url

        serviceScope.launch {
            val event = GuardFlowEvent(
                sessionId = sessionId,
                eventType = EventType.LINK_CLICKED,
                sourceApp = sourceApp,
                metadata = mapOf(
                    "url" to url,
                    "detection_method" to "accessibility_scan"
                )
            )
            repository.recordEvent(event)
            Log.d("GuardFlowObserver", ">>> RECORDED LINK: $url from $sourceApp")
        }
    }

    override fun onInterrupt() {
        Log.d("GuardFlowObserver", "Service Interrupted")
    }
}
