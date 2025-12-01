@@ -441,7 +441,7 @@ def run_script(
 ) -> Generator[ScriptDTO, None, None]:
     timeout = 5 * 60
     blocking_timeout = 1
-    lock_key = app.config.get(""REDIS_KEY_PRRFIX"") + "":run_script:"" + user_id
+    lock_key = app.config.get(""REDIS_KEY_PREFIX"") + "":run_script:"" + user_id
     lock = redis_client.lock(
         lock_key, timeout=timeout, blocking_timeout=blocking_timeout
     )