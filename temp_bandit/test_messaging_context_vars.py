@@ -1,3 +1,4 @@
+# Copyright 2024 Marimo. All rights reserved.
 from __future__ import annotations
 
 import uuid
@@ -13,7 +14,7 @@
 from marimo._runtime.requests import HTTPRequest
 
 
-class TestRunIDContext:
+class TestMessagingContextVarsRunID:
     def test_run_id_is_uuid(self):
         with run_id_context():
             run_id = RUN_ID_CTX.get()
@@ -43,7 +44,7 @@ def test_context_cleanup(self):
             RUN_ID_CTX.get()
 
 
-class TestHTTPRequestContext:
+class TestMessagingContextVarsHTTP:
     @pytest.fixture
     def mock_request(self):
         return HTTPRequest(