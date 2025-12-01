@@ -288,11 +288,26 @@ def get_column_names(self) -> list[str]:
     def get_unique_column_values(self, column: str) -> list[str | int | float]:
         return self.data[column].unique().to_list()
 
-    def get_sample_values(self, column: str) -> list[Any]:
+    def get_sample_values(self, column: str) -> list[str | int | float]:
         # Sample 3 values from the column
         SAMPLE_SIZE = 3
         try:
-            return self.data[column].head(SAMPLE_SIZE).to_list()
+            from enum import Enum
+
+            def to_primitive(value: Any) -> str | int | float:
+                if isinstance(value, list):
+                    return str([to_primitive(v) for v in value])
+                elif isinstance(value, dict):
+                    return str({k: to_primitive(v) for k, v in value.items()})
+                elif isinstance(value, Enum):
+                    return value.name
+                elif isinstance(value, (float, int)):
+                    return value
+                return str(value)
+
+            values = self.data[column].head(SAMPLE_SIZE).to_list()
+            # Serialize values to primitives
+            return [to_primitive(v) for v in values]
         except Exception:
             # May be metadata-only frame
             return []