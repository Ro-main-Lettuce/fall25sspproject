@@ -11,7 +11,14 @@
 def format_value(
     col: str, value: JSONType, format_mapping: FormatMapping
 ) -> JSONType:
-    if format_mapping is None or value is None:
+    if format_mapping is None:
+        return value
+
+    if value is None:
+        if col in format_mapping:
+            formatter = format_mapping[col]
+            if callable(formatter):
+                return formatter(value)
         return value
 
     if col in format_mapping: