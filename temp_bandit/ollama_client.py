@@ -1,9 +1,12 @@
 import requests
 import json
-from typing import List, Dict
+import os
+from typing import List, Dict, Optional
 
 class OllamaClient:
-    def __init__(self, base_url: str = ""http://localhost:11434""):
+    def __init__(self, base_url: Optional[str] = None):
+        if base_url is None:
+            base_url = os.getenv(""OLLAMA_HOST"", ""http://localhost:11434"")
         self.base_url = base_url
         self.api_url = f""{base_url}/api""
     
@@ -196,4 +199,4 @@ def main():
     print(f""AI: {response}"")
 
 if __name__ == ""__main__"":
-    main() 
\ No newline at end of file
+    main()    
\ No newline at end of file