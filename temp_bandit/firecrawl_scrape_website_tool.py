@@ -1,8 +1,11 @@
-from typing import Any, Dict, Optional, Type
+from typing import TYPE_CHECKING, Any, Dict, Optional, Type
 
-from pydantic import BaseModel, Field
+from crewai.tools import BaseTool
+from pydantic import BaseModel, ConfigDict, Field
 
-from crewai_tools.tools.base_tool import BaseTool
+# Type checking import
+if TYPE_CHECKING:
+    from firecrawl import FirecrawlApp
 
 
 class FirecrawlScrapeWebsiteToolSchema(BaseModel):
@@ -20,11 +23,14 @@ class FirecrawlScrapeWebsiteToolSchema(BaseModel):
 
 
 class FirecrawlScrapeWebsiteTool(BaseTool):
+    model_config = ConfigDict(
+        arbitrary_types_allowed=True, validate_assignment=True, frozen=False
+    )
     name: str = ""Firecrawl web scrape tool""
     description: str = ""Scrape webpages url using Firecrawl and return the contents""
     args_schema: Type[BaseModel] = FirecrawlScrapeWebsiteToolSchema
     api_key: Optional[str] = None
-    firecrawl: Optional[Any] = None
+    firecrawl: Optional[""FirecrawlApp""] = None  # Updated to use TYPE_CHECKING
 
     def __init__(self, api_key: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
@@ -57,3 +63,14 @@ def _run(
             ""timeout"": timeout,
         }
         return self.firecrawl.scrape_url(url, options)
+
+
+try:
+    from firecrawl import FirecrawlApp
+
+    # Must rebuild model after class is defined
+    FirecrawlScrapeWebsiteTool.model_rebuild()
+except ImportError:
+    """"""
+    When this tool is not used, then exception can be ignored.
+    """"""