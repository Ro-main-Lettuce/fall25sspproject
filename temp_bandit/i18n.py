@@ -4,8 +4,10 @@
 
 from pydantic import BaseModel, Field, PrivateAttr, model_validator
 
+""""""Internationalization support for CrewAI prompts and messages.""""""
 
 class I18N(BaseModel):
+    """"""Handles loading and retrieving internationalized prompts.""""""
     _prompts: Dict[str, Dict[str, str]] = PrivateAttr()
     prompt_file: Optional[str] = Field(
         default=None,