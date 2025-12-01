@@ -1,29 +1,50 @@
-from typing import Any, Optional, Type
-from pydantic import BaseModel, Field
-from pypdf import PdfReader, PdfWriter, PageObject, ContentStream, NameObject, Font
 from pathlib import Path
+from typing import Optional, Type
+
+from pydantic import BaseModel, Field
+from pypdf import ContentStream, Font, NameObject, PageObject, PdfReader, PdfWriter
 
 
 class PDFTextWritingToolSchema(BaseModel):
     """"""Input schema for PDFTextWritingTool.""""""
+
     pdf_path: str = Field(..., description=""Path to the PDF file to modify"")
     text: str = Field(..., description=""Text to add to the PDF"")
-    position: tuple = Field(..., description=""Tuple of (x, y) coordinates for text placement"")
+    position: tuple = Field(
+        ..., description=""Tuple of (x, y) coordinates for text placement""
+    )
     font_size: int = Field(default=12, description=""Font size of the text"")
-    font_color: str = Field(default=""0 0 0 rg"", description=""RGB color code for the text"")
-    font_name: Optional[str] = Field(default=""F1"", description=""Font name for standard fonts"")
-    font_file: Optional[str] = Field(None, description=""Path to a .ttf font file for custom font usage"")
+    font_color: str = Field(
+        default=""0 0 0 rg"", description=""RGB color code for the text""
+    )
+    font_name: Optional[str] = Field(
+        default=""F1"", description=""Font name for standard fonts""
+    )
+    font_file: Optional[str] = Field(
+        None, description=""Path to a .ttf font file for custom font usage""
+    )
     page_number: int = Field(default=0, description=""Page number to add text to"")
 
 
 class PDFTextWritingTool(RagTool):
     """"""A tool to add text to specific positions in a PDF, with custom font support.""""""
+
     name: str = ""PDF Text Writing Tool""
     description: str = ""A tool that can write text to a specific position in a PDF document, with optional custom font embedding.""
     args_schema: Type[BaseModel] = PDFTextWritingToolSchema
 
-    def run(self, pdf_path: str, text: str, position: tuple, font_size: int, font_color: str,
-            font_name: str = ""F1"", font_file: Optional[str] = None, page_number: int = 0, **kwargs) -> str:
+    def run(
+        self,
+        pdf_path: str,
+        text: str,
+        position: tuple,
+        font_size: int,
+        font_color: str,
+        font_name: str = ""F1"",
+        font_file: Optional[str] = None,
+        page_number: int = 0,
+        **kwargs,
+    ) -> str:
         reader = PdfReader(pdf_path)
         writer = PdfWriter()
 
@@ -63,4 +84,4 @@ def embed_font(self, writer: PdfWriter, font_file: str) -> str:
         with open(font_file, ""rb"") as file:
             font = Font.true_type(file.read())
         font_ref = writer.add_object(font)
-        return font_ref
\ No newline at end of file
+        return font_ref