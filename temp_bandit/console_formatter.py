@@ -1753,3 +1753,9 @@ def handle_guardrail_completed(
                 Attempts=f""{retry_count + 1}"",
             )
             self.print_panel(content, ""🛡️ Guardrail Failed"", ""red"")
+
+    def stop_live(self) -> None:
+        """"""Stop and clear any active Live session to restore normal terminal output.""""""
+        if self._live:
+            self._live.stop()
+            self._live = None