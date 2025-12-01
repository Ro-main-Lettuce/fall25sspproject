@@ -4,7 +4,7 @@
 
 
 class TVNews(BaseModel):
+    description: str | None = Field(None, description=""Description of the scene contents and visual elements"")
     reporters: List[str] | None = Field(None, description=""List of reporter names appearing in the news broadcast"")
     chyron: str | None = Field(None, description=""Text displayed in the lower third of the screen (chyron/news ticker)"")
-    description: str | None = Field(None, description=""Description of the scene contents and visual elements"")
     network: str | None = Field(None, description=""Name of the news network broadcasting the content"")