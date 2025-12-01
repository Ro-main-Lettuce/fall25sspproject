@@ -1,4 +1,4 @@
-from typing import Any, Optional, Type
+from typing import Any, Dict, Optional, Type, Union
 
 from embedchain.models.data_type import DataType
 from pydantic import BaseModel, Field, model_validator
@@ -9,15 +9,19 @@
 class FixedJSONSearchToolSchema(BaseModel):
     """"""Input for JSONSearchTool.""""""
 
-    search_query: Any = Field(
+    search_query: Union[str, Dict[str, Any]] = Field(
         ...,
-        description=""Mandatory search query you want to use to search the JSON's content"",
+        description=""Mandatory search query as either a string or a dictionary with 'description' key"",
     )
 
     @model_validator(mode=""after"")
     def validate_search_query(self):
-        """"""Validate and convert search_query to string if it's a dictionary.""""""
-        if isinstance(self.search_query, dict) and ""description"" in self.search_query:
+        """"""Validate and convert search_query to string format.""""""
+        if isinstance(self.search_query, dict):
+            if ""description"" not in self.search_query:
+                raise ValueError(""Dictionary input must contain a 'description' key"")
+            if not isinstance(self.search_query[""description""], str):
+                raise ValueError(""Description value must be a string"")
             self.search_query = self.search_query[""description""]
         elif not isinstance(self.search_query, str):
             raise ValueError(""search_query must be a string or a dictionary with a 'description' key"")