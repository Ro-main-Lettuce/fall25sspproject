@@ -3,10 +3,9 @@
 
 import requests
 from bs4 import BeautifulSoup
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
-from ..base_tool import BaseTool
-
 
 class FixedScrapeElementFromWebsiteToolSchema(BaseModel):
     """"""Input for ScrapeElementFromWebsiteTool.""""""