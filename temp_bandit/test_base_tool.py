@@ -15,7 +15,7 @@ def my_tool(question: str) -> str:
         my_tool.description
         == ""Tool Name: Name of my tool
Tool Arguments: {'question': {'description': None, 'type': 'str'}}
Tool Description: Clear description for what this tool is useful for, your agent will need this information to use it.""
     )
-    assert my_tool.args_schema.schema()[""properties""] == {
+    assert my_tool.args_schema.model_json_schema()[""properties""] == {
         ""question"": {""title"": ""Question"", ""type"": ""string""}
     }
     assert (
@@ -29,7 +29,7 @@ def my_tool(question: str) -> str:
         converted_tool.description
         == ""Tool Name: Name of my tool
Tool Arguments: {'question': {'description': None, 'type': 'str'}}
Tool Description: Clear description for what this tool is useful for, your agent will need this information to use it.""
     )
-    assert converted_tool.args_schema.schema()[""properties""] == {
+    assert converted_tool.args_schema.model_json_schema()[""properties""] == {
         ""question"": {""title"": ""Question"", ""type"": ""string""}
     }
     assert (
@@ -54,7 +54,7 @@ def _run(self, question: str) -> str:
         my_tool.description
         == ""Tool Name: Name of my tool
Tool Arguments: {'question': {'description': None, 'type': 'str'}}
Tool Description: Clear description for what this tool is useful for, your agent will need this information to use it.""
     )
-    assert my_tool.args_schema.schema()[""properties""] == {
+    assert my_tool.args_schema.model_json_schema()[""properties""] == {
         ""question"": {""title"": ""Question"", ""type"": ""string""}
     }
     assert my_tool.run(""What is the meaning of life?"") == ""What is the meaning of life?""
@@ -66,7 +66,7 @@ def _run(self, question: str) -> str:
         converted_tool.description
         == ""Tool Name: Name of my tool
Tool Arguments: {'question': {'description': None, 'type': 'str'}}
Tool Description: Clear description for what this tool is useful for, your agent will need this information to use it.""
     )
-    assert converted_tool.args_schema.schema()[""properties""] == {
+    assert converted_tool.args_schema.model_json_schema()[""properties""] == {
         ""question"": {""title"": ""Question"", ""type"": ""string""}
     }
     assert (