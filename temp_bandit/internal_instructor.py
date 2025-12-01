@@ -1,3 +1,4 @@
+import warnings
 from typing import Any, Optional, Type
 
 
@@ -10,12 +11,10 @@ def __init__(
         model: Type,
         agent: Optional[Any] = None,
         llm: Optional[str] = None,
-        instructions: Optional[str] = None,
     ):
         self.content = content
         self.agent = agent
         self.llm = llm
-        self.instructions = instructions
         self.model = model
         self._client = None
         self.set_instructor()
@@ -25,23 +24,19 @@ def set_instructor(self):
         if self.agent and not self.llm:
             self.llm = self.agent.function_calling_llm or self.agent.llm
 
-        # Lazy import
-        import instructor
-        from litellm import completion
+        with warnings.catch_warnings():
+            warnings.simplefilter(""ignore"", UserWarning)
+            import instructor
+            from litellm import completion
 
-        self._client = instructor.from_litellm(
-            completion,
-            mode=instructor.Mode.TOOLS,
-        )
+            self._client = instructor.from_litellm(completion)
 
     def to_json(self):
         model = self.to_pydantic()
         return model.model_dump_json(indent=2)
 
     def to_pydantic(self):
         messages = [{""role"": ""user"", ""content"": self.content}]
-        if self.instructions:
-            messages.append({""role"": ""system"", ""content"": self.instructions})
         model = self._client.chat.completions.create(
             model=self.llm.model, response_model=self.model, messages=messages
         )