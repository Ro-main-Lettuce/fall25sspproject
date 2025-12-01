@@ -8,8 +8,8 @@
 import json
 from typing import Optional
 
-import autogen
-from autogen.code_utils import execute_code
+from ... import OpenAIWrapper, filter_config
+from ...code_utils import execute_code
 
 ADD_FUNC = {
     ""type"": ""function"",
@@ -209,10 +209,8 @@ def __init__(
             raise ValueError(
                 ""When using OpenAI or Azure OpenAI endpoints, specify a non-empty 'model' either in 'llm_config' or in each config of 'config_list'.""
             )
-        self.llm_config[""config_list""] = autogen.filter_config(
-            llm_config[""config_list""], {""model"": [self.optimizer_model]}
-        )
-        self._client = autogen.OpenAIWrapper(**self.llm_config)
+        self.llm_config[""config_list""] = filter_config(llm_config[""config_list""], {""model"": [self.optimizer_model]})
+        self._client = OpenAIWrapper(**self.llm_config)
 
     def record_one_conversation(self, conversation_history: list[dict], is_satisfied: bool = None):
         """"""Record one conversation history.