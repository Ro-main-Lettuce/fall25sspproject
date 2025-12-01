@@ -104,3 +104,15 @@ class SpanAttributes:
     LLM_STREAMING_TIME_TO_GENERATE = ""gen_ai.streaming.time_to_generate""
     LLM_STREAMING_DURATION = ""gen_ai.streaming_duration""
     LLM_STREAMING_CHUNK_COUNT = ""gen_ai.streaming.chunk_count""
+
+    # HTTP-specific attributes
+    HTTP_METHOD = ""http.method""
+    HTTP_URL = ""http.url""
+    HTTP_ROUTE = ""http.route""
+    HTTP_STATUS_CODE = ""http.status_code""
+    HTTP_REQUEST_HEADERS = ""http.request.headers""
+    HTTP_RESPONSE_HEADERS = ""http.response.headers""
+    HTTP_REQUEST_BODY = ""http.request.body""
+    HTTP_RESPONSE_BODY = ""http.response.body""
+    HTTP_USER_AGENT = ""http.user_agent""
+    HTTP_REQUEST_ID = ""http.request_id""