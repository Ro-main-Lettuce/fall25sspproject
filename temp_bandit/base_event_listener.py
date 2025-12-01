@@ -5,6 +5,8 @@
 
 
 class BaseEventListener(ABC):
+    verbose: bool = False
+
     def __init__(self):
         super().__init__()
         self.setup_listeners(crewai_event_bus)