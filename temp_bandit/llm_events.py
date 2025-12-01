@@ -1,10 +1,13 @@
+import logging
 from enum import Enum
-from typing import Any, Dict, List, Optional, Union
+from typing import Any, Dict, List, Optional, Union, Type
 
 from pydantic import BaseModel, model_validator
 
 from crewai.utilities.events.base_events import BaseEvent
 
+logger = logging.getLogger(__name__)
+
 
 class LLMCallType(Enum):
     """"""Type of LLM call being made""""""
@@ -29,11 +32,40 @@ class LLMCallStartedEvent(BaseEvent):
 
     @model_validator(mode='before')
     @classmethod
-    def sanitize_tools(cls, values):
-        """"""Sanitize tools list to only include dict objects, filtering out non-dict objects like TokenCalcHandler""""""
-        if isinstance(values, dict) and 'tools' in values and values['tools'] is not None:
-            if isinstance(values['tools'], list):
-                values['tools'] = [tool for tool in values['tools'] if isinstance(tool, dict)]
+    def sanitize_tools(cls: Type[""LLMCallStartedEvent""], values: Any) -> Any:
+        """"""Sanitize tools list to only include dict objects, filtering out non-dict objects like TokenCalcHandler.
+        
+        Args:
+            values (dict): Input values dictionary containing tools and other event data.
+
+        Returns:
+            dict: Sanitized values with filtered tools list containing only valid dict objects.
+        
+        Example:
+            >>> from crewai.utilities.token_counter_callback import TokenCalcHandler
+            >>> from crewai.agents.agent_builder.utilities.base_token_process import TokenProcess
+            >>> token_handler = TokenCalcHandler(TokenProcess())
+            >>> tools = [{""name"": ""tool1""}, token_handler, {""name"": ""tool2""}]
+            >>> sanitized = cls.sanitize_tools({""tools"": tools})
+            >>> # Expected: {""tools"": [{""name"": ""tool1""}, {""name"": ""tool2""}]}
+        """"""
+        try:
+            if isinstance(values, dict) and 'tools' in values and values['tools'] is not None:
+                if isinstance(values['tools'], list):
+                    sanitized_tools = []
+                    for tool in values['tools']:
+                        if isinstance(tool, dict):
+                            if all(isinstance(v, (str, int, float, bool, dict, list, type(None))) for v in tool.values()):
+                                sanitized_tools.append(tool)
+                            else:
+                                logger.warning(f""Tool dict contains invalid value types: {tool}"")
+                        else:
+                            logger.debug(f""Filtering out non-dict tool object: {type(tool).__name__}"")
+                    
+                    values['tools'] = sanitized_tools
+        except Exception as e:
+            logger.warning(f""Error during tools sanitization: {e}"")
+        
         return values
 
 