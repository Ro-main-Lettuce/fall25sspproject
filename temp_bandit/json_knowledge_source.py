@@ -1,19 +1,19 @@
 import json
 from pathlib import Path
-from typing import Any, Dict, List
+from typing import Any
 
 from crewai.knowledge.source.base_file_knowledge_source import BaseFileKnowledgeSource
 
 
 class JSONKnowledgeSource(BaseFileKnowledgeSource):
     """"""A knowledge source that stores and queries JSON file content using embeddings.""""""
 
-    def load_content(self) -> Dict[Path, str]:
+    def load_content(self) -> dict[Path, str]:
         """"""Load and preprocess JSON file content.""""""
-        content: Dict[Path, str] = {}
+        content: dict[Path, str] = {}
         for path in self.safe_file_paths:
             path = self.convert_to_path(path)
-            with open(path, ""r"", encoding=""utf-8"") as json_file:
+            with open(path, encoding=""utf-8"") as json_file:
                 data = json.load(json_file)
             content[path] = self._json_to_text(data)
         return content
@@ -29,12 +29,11 @@ def _json_to_text(self, data: Any, level: int = 0) -> str:
             for item in data:
                 text += f""{indent}- {self._json_to_text(item, level + 1)}
""
         else:
-            text += f""{str(data)}""
+            text += f""{data!s}""
         return text
 
     def add(self) -> None:
-        """"""
-        Add JSON file content to the knowledge source, chunk it, compute embeddings,
+        """"""Add JSON file content to the knowledge source, chunk it, compute embeddings,
         and save the embeddings.
         """"""
         content_str = (
@@ -44,7 +43,7 @@ def add(self) -> None:
         self.chunks.extend(new_chunks)
         self._save_documents()
 
-    def _chunk_text(self, text: str) -> List[str]:
+    def _chunk_text(self, text: str) -> list[str]:
         """"""Utility method to split text into chunks.""""""
         return [
             text[i : i + self.chunk_size]