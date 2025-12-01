@@ -127,6 +127,7 @@ def scan_pageserver_log_for_errors(
     # Tests run in dev mode
     "".*Starting in dev mode.*"",
     "".*Starting in dev mode - authentication security checks are disabled.*"",
+    "".*Starting in dev mode: this may be an insecure configuration.*"",
     # Tests that stop endpoints & use the storage controller's neon_local notification
     # mechanism might fail (neon_local's stopping and endpoint isn't atomic wrt the storage
     # controller's attempts to notify the endpoint).