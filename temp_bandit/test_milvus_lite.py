@@ -1,37 +1,38 @@
+# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
+
 import os
+
 from pymilvus import MilvusClient, connections
 
+
 def test_milvus_lite():
     print(""Testing Milvus Lite functionality..."")
-    
+
     # Create a test database file path
     db_path = ""./test_milvus.db""
-    
+
     try:
         # Try the new style client first
         print(""
Testing MilvusClient approach:"")
         client = MilvusClient(
             uri=f""lite://{db_path}"",
-            token=""""  # No token needed for lite
+            token="""",  # No token needed for lite
         )
         print(""✓ Successfully created MilvusClient with lite:// URI"")
-        
+
     except Exception as e:
         print(f""× MilvusClient approach failed: {str(e)}"")
-    
+
     try:
         # Try the connections approach
         print(""
Testing connections approach:"")
-        connections.connect(
-            alias=""default"",
-            uri=f""lite://{db_path}""
-        )
+        connections.connect(alias=""default"", uri=f""lite://{db_path}"")
         print(""✓ Successfully connected using connections.connect()"")
         connections.disconnect(""default"")
-        
+
     except Exception as e:
         print(f""× Connections approach failed: {str(e)}"")
-    
+
     # Clean up test database if it exists
     if os.path.exists(db_path):
         try:
@@ -40,5 +41,6 @@ def test_milvus_lite():
         except Exception as e:
             print(f""Failed to clean up test database: {str(e)}"")
 
+
 if __name__ == ""__main__"":
     test_milvus_lite()