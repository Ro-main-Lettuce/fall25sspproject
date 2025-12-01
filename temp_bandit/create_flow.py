@@ -5,7 +5,7 @@
 from crewai.telemetry import Telemetry
 
 
-def create_flow(name):
+def create_flow(name) -> None:
     """"""Create a new flow.""""""
     folder_name = name.replace("" "", ""_"").replace(""-"", ""_"").lower()
     class_name = name.replace(""_"", "" "").replace(""-"", "" "").title().replace("" "", """")
@@ -43,12 +43,12 @@ def create_flow(name):
         ""poem_crew"",
     ]
 
-    def process_file(src_file, dst_file):
+    def process_file(src_file, dst_file) -> None:
         if src_file.suffix in ["".pyc"", "".pyo"", "".pyd""]:
             return
 
         try:
-            with open(src_file, ""r"", encoding=""utf-8"") as file:
+            with open(src_file, encoding=""utf-8"") as file:
                 content = file.read()
         except Exception as e:
             click.secho(f""Error processing file {src_file}: {e}"", fg=""red"")