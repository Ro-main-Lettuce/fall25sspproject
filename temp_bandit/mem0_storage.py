@@ -48,7 +48,7 @@ def __init__(self, type, crew=None, config=None):
                 self.memory = MemoryClient(api_key=mem0_api_key)
         else:
             if mem0_local_config and len(mem0_local_config):
-                self.memory = Memory.from_config(config)
+                self.memory = Memory.from_config(mem0_local_config)
             else:
                 self.memory = Memory()
 