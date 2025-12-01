@@ -5,16 +5,28 @@
 import json
 import typing as t
 import warnings
+from inspect import Signature
 
 import typing_extensions as te
 from phi.tools.toolkit import Toolkit
 from pydantic import validate_call
+from typing_extensions import Protocol
 
 from composio import Action, ActionType, AppType
 from composio import ComposioToolSet as BaseComposioToolSet
 from composio import TagType
 from composio.tools.toolset import ProcessorsType
-from composio.utils import help_msg
+from composio.utils import help_msg, shared
+
+
+class ToolFunction(Protocol):
+    """"""Protocol for tool functions with required attributes.""""""
+
+    __signature__: Signature
+    __annotations__: t.Dict[str, t.Any]
+    __doc__: str
+
+    def __call__(self, *args: t.Any, **kwargs: t.Any) -> str: ...
 
 
 class ComposioToolSet(
@@ -42,37 +54,51 @@ def _wrap_tool(
         # Create a new Toolkit instance
         toolkit = Toolkit(name=name)
 
-        @validate_call
-        def function(**kwargs: t.Any) -> str:
-            """"""Composio tool wrapped as Phidata `Function`.
+        # Get function parameters from schema
+        params = shared.get_signature_format_from_schema_params(parameters)
 
-            Args:
-                **kwargs: Function parameters based on the schema
+        # Create function signature and annotations
+        sig = Signature(parameters=params)
+        annotations = {p.name: p.annotation for p in params}
+        annotations[""return""] = str  # Add return type annotation
+
+        @validate_call
+        def function_template(*args, **kwargs) -> str:
+            # Bind the arguments to the signature
+            bound_args = sig.bind(*args, **kwargs)
+            bound_args.apply_defaults()
 
-            Returns:
-                str: JSON string containing the function execution result
-            """"""
             return json.dumps(
                 self.execute_action(
                     action=Action(value=name),
-                    params=kwargs,
+                    params=bound_args.arguments,
                     entity_id=entity_id or self.entity_id,
                     _check_requested_actions=True,
                 )
             )
 
-        # Set function docstring from schema
-        param_docs = []
+        # Cast the function to our Protocol type to satisfy mypy
+        func = t.cast(ToolFunction, function_template)
+
+        # Apply the signature and annotations to the function
+        func.__signature__ = sig
+        func.__annotations__ = annotations
+
+        # Format docstring in Phidata standard format
+        docstring_parts = [description, ""
Args:""]
         if ""properties"" in parameters:
             for param_name, param_info in parameters[""properties""].items():
                 param_desc = param_info.get(""description"", ""No description available"")
                 param_type = param_info.get(""type"", ""any"")
-                param_docs.append(f"":param {param_name}: {param_desc} ({param_type})"")
+                docstring_parts.append(f""    {param_name} ({param_type}): {param_desc}"")
 
-        function.__doc__ = f""{description}

"" + ""
"".join(param_docs)
+        docstring_parts.append(
+            ""
Returns:
    str: JSON string containing the function execution result""
+        )
+        func.__doc__ = ""
"".join(docstring_parts)
 
         # Register the function with the toolkit
-        toolkit.register(function)
+        toolkit.register(func)
 
         return toolkit
 