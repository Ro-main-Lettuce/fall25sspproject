@@ -11,7 +11,7 @@
 from crewai.memory.user.user_memory import UserMemory
 
 
-class CustomStorage(Storage):
+class CustomStorage(Storage[Any]):
     """"""Custom storage implementation for testing.""""""
 
     def __init__(self):
@@ -141,7 +141,7 @@ def test_custom_storage_with_memory_config():
 def test_custom_storage_error_handling():
     """"""Test error handling with custom storage.""""""
     # Test exception propagation
-    class ErrorStorage(Storage):
+    class ErrorStorage(Storage[Any]):
         """"""Storage implementation that raises exceptions.""""""
         def __init__(self):
             self.data = []
@@ -172,7 +172,7 @@ def reset(self) -> None:
 
 def test_custom_storage_edge_cases():
     """"""Test edge cases with custom storage.""""""
-    class EdgeCaseStorage(Storage):
+    class EdgeCaseStorage(Storage[Any]):
         """"""Storage implementation for testing edge cases.""""""
         def __init__(self):
             self.data = []