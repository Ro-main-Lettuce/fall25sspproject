@@ -1,8 +1,11 @@
-from typing import Any, Dict, Optional, Type
+from typing import TYPE_CHECKING, Any, Dict, Optional, Type
 
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
-from crewai_tools.tools.base_tool import BaseTool
+# Type checking import
+if TYPE_CHECKING:
+    from firecrawl import FirecrawlApp
 
 
 class FirecrawlSearchToolSchema(BaseModel):
@@ -20,7 +23,7 @@ class FirecrawlSearchTool(BaseTool):
     description: str = ""Search webpages using Firecrawl and return the results""
     args_schema: Type[BaseModel] = FirecrawlSearchToolSchema
     api_key: Optional[str] = None
-    firecrawl: Optional[Any] = None
+    firecrawl: Optional[""FirecrawlApp""] = None
 
     def __init__(self, api_key: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
@@ -45,4 +48,4 @@ def _run(
             result_options = {}
 
         options = {""pageOptions"": page_options, ""resultOptions"": result_options}
-        return self.firecrawl.search(query, options)
+        return self.firecrawl.search(query, **options)