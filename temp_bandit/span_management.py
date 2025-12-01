@@ -157,7 +157,7 @@ def safe_set_attribute(span: Span, key: str, value: Any, max_length: int = 1000)
     try:
         span.set_attribute(key, value)
     except Exception as e:
-        logger.debug(f""Failed to set span attribute {key}: {e}"")
+        logger.warning(f""Failed to set span attribute {key}: {e}"")
 
 
 def get_span_context_info(span: Optional[Span] = None) -> Tuple[str, str]: