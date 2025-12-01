@@ -11,10 +11,14 @@
 
 from pydantic import BaseModel, Extra, root_validator
 
-from autogen._pydantic import PYDANTIC_V1
-from autogen.agentchat import Agent, UserProxyAgent
-from autogen.code_utils import UNKNOWN, execute_code, extract_code, infer_lang
-from autogen.math_utils import get_answer
+from ..._pydantic import PYDANTIC_V1
+from ...code_utils import UNKNOWN, execute_code, extract_code, infer_lang
+from ...import_utils import optional_import_block, require_optional_import
+from ...math_utils import get_answer
+from .. import Agent, UserProxyAgent
+
+with optional_import_block() as result:
+    import wolframalpha
 
 PROMPTS = {
     # default
@@ -402,16 +406,12 @@ class Config:
 
     @root_validator(skip_on_failure=True)
     @classmethod
+    @require_optional_import(""wolframalpha"", ""mathchat"")
     def validate_environment(cls, values: dict) -> dict:
         """"""Validate that api key and python package exists in environment.""""""
         wolfram_alpha_appid = get_from_dict_or_env(values, ""wolfram_alpha_appid"", ""WOLFRAM_ALPHA_APPID"")
         values[""wolfram_alpha_appid""] = wolfram_alpha_appid
 
-        try:
-            import wolframalpha
-
-        except ImportError as e:
-            raise ImportError(""wolframalpha is not installed. Please install it with `pip install wolframalpha`"") from e
         client = wolframalpha.Client(wolfram_alpha_appid)
         values[""wolfram_client""] = client
 