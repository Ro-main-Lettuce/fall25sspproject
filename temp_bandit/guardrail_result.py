@@ -1,11 +1,10 @@
-""""""
-Module for handling task guardrail validation results.
+""""""Module for handling task guardrail validation results.
 
 This module provides the GuardrailResult class which standardizes
 the way task guardrails return their validation results.
 """"""
 
-from typing import Any, Optional, Tuple, Union
+from typing import Any
 
 from pydantic import BaseModel, field_validator
 
@@ -21,24 +20,28 @@ class GuardrailResult(BaseModel):
         success (bool): Whether the guardrail validation passed
         result (Any, optional): The validated/transformed result if successful
         error (str, optional): Error message if validation failed
+
     """"""
+
     success: bool
-    result: Optional[Any] = None
-    error: Optional[str] = None
+    result: Any | None = None
+    error: str | None = None
 
     @field_validator(""result"", ""error"")
     @classmethod
     def validate_result_error_exclusivity(cls, v: Any, info) -> Any:
         values = info.data
         if ""success"" in values:
             if values[""success""] and v and ""error"" in values and values[""error""]:
-                raise ValueError(""Cannot have both result and error when success is True"")
+                msg = ""Cannot have both result and error when success is True""
+                raise ValueError(msg)
             if not values[""success""] and v and ""result"" in values and values[""result""]:
-                raise ValueError(""Cannot have both result and error when success is False"")
+                msg = ""Cannot have both result and error when success is False""
+                raise ValueError(msg)
         return v
 
     @classmethod
-    def from_tuple(cls, result: Tuple[bool, Union[Any, str]]) -> ""GuardrailResult"":
+    def from_tuple(cls, result: tuple[bool, Any | str]) -> ""GuardrailResult"":
         """"""Create a GuardrailResult from a validation tuple.
 
         Args:
@@ -47,10 +50,11 @@ def from_tuple(cls, result: Tuple[bool, Union[Any, str]]) -> ""GuardrailResult"":
 
         Returns:
             GuardrailResult: A new instance with the tuple data.
+
         """"""
         success, data = result
         return cls(
             success=success,
             result=data if success else None,
-            error=data if not success else None
+            error=data if not success else None,
         )