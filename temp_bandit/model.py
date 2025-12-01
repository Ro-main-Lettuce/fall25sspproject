@@ -108,15 +108,15 @@ def _set_prompt_attributes(attributes: AttributeMap, args: Tuple, kwargs: Dict[s
                         role = item.role
                     attributes[MessageAttributes.PROMPT_ROLE.format(i=i)] = role
             except Exception as e:
-                logger.debug(f""Error extracting prompt content at index {i}: {e}"")
+                logger.warning(f""Error extracting prompt content at index {i}: {e}"")
     else:
         try:
             extracted_text = _extract_content_from_prompt(content)
             if extracted_text:
                 attributes[MessageAttributes.PROMPT_CONTENT.format(i=0)] = extracted_text
                 attributes[MessageAttributes.PROMPT_ROLE.format(i=0)] = ""user""
         except Exception as e:
-            logger.debug(f""Error extracting prompt content: {e}"")
+            logger.warning(f""Error extracting prompt content: {e}"")
 
 
 def _set_response_attributes(attributes: AttributeMap, response: Any) -> None:
@@ -163,7 +163,7 @@ def _set_response_attributes(attributes: AttributeMap, response: Any) -> None:
                 if hasattr(candidate, ""finish_reason""):
                     attributes[MessageAttributes.COMPLETION_FINISH_REASON.format(i=i)] = candidate.finish_reason
     except Exception as e:
-        logger.debug(f""Error extracting completion content: {e}"")
+        logger.warning(f""Error extracting completion content: {e}"")
 
 
 def get_model_attributes(