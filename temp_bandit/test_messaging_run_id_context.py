@@ -1,10 +1,13 @@
+# Copyright 2024 Marimo. All rights reserved.
+from __future__ import annotations
+
 import pytest
 
 from marimo._messaging.context import RUN_ID_CTX, run_id_context
 
 
-class TestRunIDContext:
-    def test_run_id_context(self):
+class TestMessagingRunIDContext:
+    def test_run_id_context(self) -> None:
         with run_id_context():
             run_id = RUN_ID_CTX.get()
             assert run_id is not None, (