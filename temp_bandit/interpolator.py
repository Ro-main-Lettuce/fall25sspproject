@@ -66,22 +66,30 @@ def bake(self, application: ApplicationOut, output_dir: str, overwrite: bool = F
 
         # TODO: optimize overwriting some files below of user wants to update only some handlers / capabilities / etc
         with open(os.path.join(output_dir, ""tsp_schema"", ""main.tsp""), ""a"") as f:
-            f.write(application.typespec.typespec_definitions)
+            f.write(application.typespec.typespec_definitions or """")
 
         with open(os.path.join(output_dir, ""app_schema"", ""src"", ""db"", ""schema"", ""application.ts""), ""w"") as f:
-            f.write(application.drizzle.drizzle_schema)
+            if application.drizzle is not None:
+                f.write(application.drizzle.drizzle_schema or """")
+            else:
+                f.write("""")
 
         with open(os.path.join(output_dir, ""app_schema"", ""src"", ""common"", ""schema.ts""), ""w"") as f:
-            f.write(application.typescript_schema.typescript_schema)
-
-        handler_tools = [
-            {
-                ""name"": name,
-                ""description"": next((f.description for f in application.typespec.llm_functions if f.name == name), """"),
-                ""argument_schema"": f""schema.{handler.argument_schema}"",
-            }
-            for name, handler in application.handlers.items()
-        ]
+            if application.typescript_schema is not None:
+                f.write(application.typescript_schema.typescript_schema or """")
+            else:
+                f.write("""")
+
+        handler_tools = []
+        if application.typespec.llm_functions is not None and application.handlers is not None:
+            handler_tools = [
+                {
+                    ""name"": name,
+                    ""description"": next((f.description for f in application.typespec.llm_functions if f.name == name), """"),
+                    ""argument_schema"": f""schema.{handler.argument_schema}"",
+                }
+                for name, handler in application.handlers.items()
+            ]
 
         capability_list = []
         if application.capabilities is not None:
@@ -95,14 +103,16 @@ def bake(self, application: ApplicationOut, output_dir: str, overwrite: bool = F
         with open(os.path.join(output_dir, ""app_schema"", ""src"", ""custom_tools.ts""), ""w"") as f:
             f.write(self.environment.from_string(CUSTOM_TOOL_TEMPLATE).render(handlers=custom_tools))
 
-        for name, handler in application.handlers.items():
-            with open(os.path.join(output_dir, ""app_schema"", ""src"", ""handlers"", f""{name}.ts""), ""w"") as f:
-                if handler.handler:
-                    f.write(handler.handler)
-                else:
-                    logger.error(f""Handler {name} does not have a handler function"")
-                    f.write(f""/// handler code was not generated"")
-
-        for name, handler_test in application.handler_tests.items():
-            with open(os.path.join(output_dir, ""app_schema"", ""src"", ""tests"", ""handlers"", f""{name}.test.ts""), ""w"") as f:
-                f.write(handler_test.content)
+        if application.handlers is not None:
+            for name, handler in application.handlers.items():
+                with open(os.path.join(output_dir, ""app_schema"", ""src"", ""handlers"", f""{name}.ts""), ""w"") as f:
+                    if handler.handler:
+                        f.write(handler.handler)
+                    else:
+                        logger.error(f""Handler {name} does not have a handler function"")
+                        f.write(f""/// handler code was not generated"")
+
+        if application.handler_tests is not None:
+            for name, handler_test in application.handler_tests.items():
+                with open(os.path.join(output_dir, ""app_schema"", ""src"", ""tests"", ""handlers"", f""{name}.test.ts""), ""w"") as f:
+                    f.write(handler_test.content or """")