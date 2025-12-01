@@ -10,7 +10,7 @@ class LLMContextLengthExceededException(Exception):
         ""exceeds token limit"",
     ]
 
-    def __init__(self, error_message: str):
+    def __init__(self, error_message: str) -> None:
         self.original_error_message = error_message
         super().__init__(self._get_error_message(error_message))
 
@@ -20,7 +20,7 @@ def _is_context_limit_error(self, error_message: str) -> bool:
             for phrase in self.CONTEXT_LIMIT_ERRORS
         )
 
-    def _get_error_message(self, error_message: str):
+    def _get_error_message(self, error_message: str) -> str:
         return (
             f""LLM context length exceeded. Original error: {error_message}
""
             ""Consider using a smaller input or implementing a text splitting strategy.""