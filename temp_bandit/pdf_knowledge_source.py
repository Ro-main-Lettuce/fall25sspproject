@@ -1,13 +1,12 @@
 from pathlib import Path
-from typing import Dict, List
 
 from crewai.knowledge.source.base_file_knowledge_source import BaseFileKnowledgeSource
 
 
 class PDFKnowledgeSource(BaseFileKnowledgeSource):
     """"""A knowledge source that stores and queries PDF file content using embeddings.""""""
 
-    def load_content(self) -> Dict[Path, str]:
+    def load_content(self) -> dict[Path, str]:
         """"""Load and preprocess PDF file content.""""""
         pdfplumber = self._import_pdfplumber()
 
@@ -31,21 +30,21 @@ def _import_pdfplumber(self):
 
             return pdfplumber
         except ImportError:
+            msg = ""pdfplumber is not installed. Please install it with: pip install pdfplumber""
             raise ImportError(
-                ""pdfplumber is not installed. Please install it with: pip install pdfplumber""
+                msg,
             )
 
     def add(self) -> None:
-        """"""
-        Add PDF file content to the knowledge source, chunk it, compute embeddings,
+        """"""Add PDF file content to the knowledge source, chunk it, compute embeddings,
         and save the embeddings.
         """"""
-        for _, text in self.content.items():
+        for text in self.content.values():
             new_chunks = self._chunk_text(text)
             self.chunks.extend(new_chunks)
         self._save_documents()
 
-    def _chunk_text(self, text: str) -> List[str]:
+    def _chunk_text(self, text: str) -> list[str]:
         """"""Utility method to split text into chunks.""""""
         return [
             text[i : i + self.chunk_size]