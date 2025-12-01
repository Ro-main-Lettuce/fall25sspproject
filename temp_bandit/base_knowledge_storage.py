@@ -1,5 +1,5 @@
 from abc import ABC, abstractmethod
-from typing import Any, Dict, List, Optional
+from typing import Any
 
 
 class BaseKnowledgeStorage(ABC):
@@ -8,22 +8,19 @@ class BaseKnowledgeStorage(ABC):
     @abstractmethod
     def search(
         self,
-        query: List[str],
+        query: list[str],
         limit: int = 3,
-        filter: Optional[dict] = None,
+        filter: dict | None = None,
         score_threshold: float = 0.35,
-    ) -> List[Dict[str, Any]]:
+    ) -> list[dict[str, Any]]:
         """"""Search for documents in the knowledge base.""""""
-        pass
 
     @abstractmethod
     def save(
-        self, documents: List[str], metadata: Dict[str, Any] | List[Dict[str, Any]]
+        self, documents: list[str], metadata: dict[str, Any] | list[dict[str, Any]],
     ) -> None:
         """"""Save documents to the knowledge base.""""""
-        pass
 
     @abstractmethod
     def reset(self) -> None:
         """"""Reset the knowledge base.""""""
-        pass