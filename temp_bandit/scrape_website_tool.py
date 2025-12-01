@@ -1,12 +1,12 @@
 import os
+import re
 from typing import Any, Optional, Type
 
 import requests
 from bs4 import BeautifulSoup
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
-from ..base_tool import BaseTool
-
 
 class FixedScrapeWebsiteToolSchema(BaseModel):
     """"""Input for ScrapeWebsiteTool.""""""
@@ -65,7 +65,7 @@ def _run(
         page.encoding = page.apparent_encoding
         parsed = BeautifulSoup(page.text, ""html.parser"")
 
-        text = parsed.get_text()
-        text = ""
"".join([i for i in text.split(""
"") if i.strip() != """"])
-        text = "" "".join([i for i in text.split("" "") if i.strip() != """"])
+        text = parsed.get_text("" "")
+        text = re.sub(""[ \t]+"", "" "", text)
+        text = re.sub(""\\s+
\\s+"", ""
"", text)
         return text