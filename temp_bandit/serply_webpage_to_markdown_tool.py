@@ -18,9 +18,7 @@ class SerplyWebpageToMarkdownToolSchema(BaseModel):
 
 class SerplyWebpageToMarkdownTool(RagTool):
     name: str = ""Webpage to Markdown""
-    description: str = (
-        ""A tool to perform convert a webpage to markdown to make it easier for LLMs to understand""
-    )
+    description: str = ""A tool to perform convert a webpage to markdown to make it easier for LLMs to understand""
     args_schema: Type[BaseModel] = SerplyWebpageToMarkdownToolSchema
     request_url: str = ""https://api.serply.io/v1/request""
     proxy_location: Optional[str] = ""US""