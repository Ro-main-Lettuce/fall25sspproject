@@ -15,6 +15,8 @@
 
 
 class GenericRequest(BaseModel):
+    """"""A generic request model for LLM API requests.""""""
+
     model: str
     messages: List[Dict[str, Any]]
     response_format: Dict[str, Any] | None = None