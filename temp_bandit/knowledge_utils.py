@@ -1,7 +1,7 @@
-from typing import Any, Dict, List
+from typing import Any
 
 
-def extract_knowledge_context(knowledge_snippets: List[Dict[str, Any]]) -> str:
+def extract_knowledge_context(knowledge_snippets: list[dict[str, Any]]) -> str:
     """"""Extract knowledge from the task prompt.""""""
     valid_snippets = [
         result[""context""]