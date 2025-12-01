@@ -228,6 +228,9 @@ def merge(self, other: ""TSDict"") -> ""TSDict"":
             with get_codebase_session(tmpdir=tmpdir, files={""temp.ts"": f""let temp = {merged_source}""}, programming_language=ProgrammingLanguage.TYPESCRIPT) as codebase:
                 file = codebase.get_file(""temp.ts"")
                 temp = file.get_symbol(""temp"")
+                if temp is None:
+                    msg = ""Failed to get symbol 'temp' from temporary file""
+                    raise ValueError(msg)
                 return temp.value
 
     @reader