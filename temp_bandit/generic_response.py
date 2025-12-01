@@ -25,6 +25,8 @@
 
 
 class GenericResponse(BaseModel):
+    """"""A generic response model for LLM API requests.""""""
+
     response_message: Optional[Dict[str, Any]] | str = None
     response_errors: Optional[List[str]] = None
     raw_response: Optional[Dict[str, Any]]