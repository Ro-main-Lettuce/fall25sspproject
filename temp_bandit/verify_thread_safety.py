@@ -6,7 +6,6 @@
 import sys
 import os
 import threading
-import time
 from concurrent.futures import ThreadPoolExecutor
 
 sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
@@ -86,7 +85,7 @@ def emit_events(thread_id, num_events=10):
             print(f""✅ Thread safety test passed - each handler received {expected_total} events"")
             return True
         else:
-            print(f""❌ Thread safety test failed"")
+            print(""❌ Thread safety test failed"")
             print(f""Handler1 received {len(handler1_events)} events, expected {expected_total}"")
             print(f""Handler2 received {len(handler2_events)} events, expected {expected_total}"")
             return False