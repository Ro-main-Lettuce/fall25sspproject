@@ -114,7 +114,7 @@ def _extract_from_crewai_format(token_usage_str: str) -> TokenUsage:
             usage.cached_prompt_tokens = metrics.get(""cached_prompt_tokens"")
 
         except Exception as e:
-            logger.debug(f""Failed to parse CrewAI token usage: {e}"")
+            logger.warning(f""Failed to parse CrewAI token usage: {e}"")
 
         return usage
 