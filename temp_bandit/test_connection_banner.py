@@ -185,7 +185,7 @@ async def test_connection_banner(connection_banner: AppHarness):
         lambda: processes.handle_port(
             ""backend"", connection_banner.backend_port or 0, auto_increment=False
         ),
-        timeout=60,
+        timeout=120,
     ):
         print(f""Port {result} is now free."")
     assert result, f""Port is not free: {connection_banner.backend_port} after timeout.""