@@ -29,7 +29,7 @@ def safe_parse(content: str) -> Optional[Dict[str, Any]]:
         return json.loads(content)
     except (json.JSONDecodeError, TypeError, ValueError):
         # If parsing fails, log a debug message and return None
-        logger.debug(f""Failed to parse JSON content: {content[:100]}..."")
+        logger.warning(f""Failed to parse JSON content: {content[:100]}..."")
         return None
 
 
@@ -202,7 +202,7 @@ def has_key(obj, key):
                                         # Process this usage data recursively
                                         return process_token_usage(parsed_text[""usage""], attributes)
         except Exception as e:
-            logger.debug(f""Error during deep token extraction: {e}"")
+            logger.warning(f""Error during deep token extraction: {e}"")
 
     return result
 