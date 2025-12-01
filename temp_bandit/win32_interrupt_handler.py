@@ -10,7 +10,9 @@
 
 
 class Win32InterruptHandler(threading.Thread):
-    def __init__(self, interrupt_queue: ""Queue[bool | type[KeyboardInterrupt]]"") -> None:
+    def __init__(
+        self, interrupt_queue: ""Queue[bool | type[KeyboardInterrupt]]""
+    ) -> None:
         super(Win32InterruptHandler, self).__init__()
         self.daemon = True
         self.interrupt_queue = interrupt_queue