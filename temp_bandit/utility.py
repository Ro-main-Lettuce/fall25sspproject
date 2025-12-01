@@ -160,3 +160,57 @@ def _record_entity_output(span: trace.Span, result: Any, entity_kind: str = ""ent
             logger.debug(""Operation output exceeds size limit, not recording"")
     except Exception as err:
         logger.warning(f""Failed to serialize operation output: {err}"")
+
+
+# Helper functions for HTTP request/response data extraction
+
+
+def _extract_request_data():
+    """"""Extract HTTP request data from the current web framework context.""""""
+    request_data = {}
+
+    try:
+        # Try to import Flask and get current request
+        from flask import request
+
+        request_data = {
+            ""method"": request.method,
+            ""url"": request.url,
+            ""headers"": dict(request.headers),
+            ""args"": dict(request.args),
+            ""form"": dict(request.form) if request.form else None,
+            ""json"": request.get_json(silent=True),
+            ""data"": request.get_data(as_text=True) if request.content_length else None,
+        }
+    except ImportError:
+        logger.debug(""Flask not available for request data extraction"")
+    except Exception as e:
+        logger.warning(f""Failed to extract request data: {e}"")
+
+    return request_data
+
+
+def _extract_response_data(response):
+    """"""Extract HTTP response data from response object.""""""
+    response_data = {}
+
+    try:
+        # Handle Flask response objects
+        from flask import Response
+
+        if isinstance(response, Response):
+            response_data = {
+                ""status_code"": response.status_code,
+                ""headers"": dict(response.headers),
+                ""data"": response.get_data(as_text=True) if response.content_length else None,
+            }
+        else:
+            # Handle cases where response is just data (will be converted to Response by Flask)
+            response_data = {
+                ""status_code"": 200,  # Default status for successful responses
+                ""data"": str(response) if response is not None else None,
+            }
+    except Exception as e:
+        logger.warning(f""Failed to extract response data: {e}"")
+
+    return response_data