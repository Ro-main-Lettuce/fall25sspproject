@@ -2,7 +2,6 @@
 from crewai.llm import LLM
 from typing import Type, Optional
 from pydantic import BaseModel, Field
-import os
 from pathlib import Path
 
 
@@ -63,7 +62,7 @@ def _run(self, file_path: str, edit_instructions: str, context: Optional[str] =
             new_content = self._extract_file_content(response)
             
             if new_content is None:
-                return f""Error: Failed to generate valid file content. LLM response was malformed.""
+                return ""Error: Failed to generate valid file content. LLM response was malformed.""
             
             backup_path = f""{file_path}.backup""
             with open(backup_path, 'w', encoding='utf-8') as f: