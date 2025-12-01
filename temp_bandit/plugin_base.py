@@ -1,5 +1,6 @@
 import asyncio
 import inspect
+import threading
 from abc import ABC, abstractmethod
 from typing import List, Any, TypeVar, Generic
 
@@ -103,6 +104,30 @@ def _execute_tool(
         Returns:
             The result of the tool execution
         """"""
+
+        def _run_coroutine_in_new_thread(coro):
+            """"""Run a coroutine in a new thread with its own event loop.""""""
+            result = None
+            exception = None
+            
+            def run_coro():
+                nonlocal result, exception
+                loop = asyncio.new_event_loop()
+                try:
+                    result = loop.run_until_complete(coro)
+                except Exception as e:
+                    exception = e
+                finally:
+                    loop.close()
+            
+            thread = threading.Thread(target=run_coro)
+            thread.start()
+            thread.join()
+            
+            if exception:
+                raise exception
+            return result
+
         wallet_client_index = tool_metadata.wallet_client.get(""index"", 0)
         parameters_index = tool_metadata.parameters.get(""index"", 0)
         args = [None] * max(wallet_client_index or 0, parameters_index)
@@ -116,6 +141,20 @@ def _execute_tool(
         method = getattr(tool_provider, tool_metadata.target.__name__)
         result = method(*args)
 
+        # Handle coroutine results in three cases:
+        # 1. If there's an existing event loop and it's not running: use it directly with run_until_complete
+        # 2. If there's an existing event loop and it's running: create a new thread with its own event loop to avoid deadlock
+        # 3. If there's no event loop: create a new one and use it, then set it as the current event loop to be reused
         if inspect.iscoroutine(result):
-            return asyncio.get_event_loop().run_until_complete(result)
+            try:
+                loop = asyncio.get_event_loop()
+                if loop.is_running():
+                    return _run_coroutine_in_new_thread(result)
+                else:
+                    return loop.run_until_complete(result)
+            except RuntimeError:
+                loop = asyncio.new_event_loop()
+                asyncio.set_event_loop(loop)
+                return loop.run_until_complete(result)
+
         return result