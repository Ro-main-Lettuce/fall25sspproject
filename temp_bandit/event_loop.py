@@ -4,10 +4,7 @@
 
 
 def run_in_event_loop(coroutine):
-    """"""
-    Run a coroutine in the current event loop or create a new one if there isn't one.
-    """"""
-
+    """"""Run a coroutine in the current event loop or create a new one if there isn't one.""""""
     try:
         # This call will raise an RuntimError if there is no event loop running.
         asyncio.get_running_loop()
@@ -18,7 +15,7 @@ def run_in_event_loop(coroutine):
         nest_asyncio.apply()
 
         return asyncio.run(coroutine)
-    except RuntimeError as e:
+    except RuntimeError:
         # Explicitly pass, since we want to fallback to asyncio.run
         pass
 