@@ -5,7 +5,7 @@
 from typing import List, Dict, Optional, Tuple
 
 class ChatDatabase:
-    def __init__(self, db_path: str = ""backend/chat_data.db""):
+    def __init__(self, db_path: str = ""/app/backend/chat_data.db""):
         self.db_path = db_path
         self.init_database()
     
@@ -681,4 +681,4 @@ def generate_session_title(first_message: str, max_length: int = 50) -> str:
     stats = db.get_stats()
     print(f""📊 Stats: {stats}"")
     
-    print(""✅ Database test completed!"") 
\ No newline at end of file
+    print(""✅ Database test completed!"")  
\ No newline at end of file