@@ -1,4 +1,5 @@
 """"""Module for documenting Reflex environment variables.""""""
+
 from __future__ import annotations
 
 import inspect
@@ -12,70 +13,86 @@
 
 class EnvVarDocs:
     """"""Documentation for Reflex environment variables.""""""
-    
+
     @classmethod
     def get_all_env_vars(cls) -> List[Tuple[str, Any]]:
         """"""Get all environment variables from the environment class.
-        
+
         Returns:
             A list of tuples containing the environment variable name and its EnvVar instance.
         """"""
         env_vars = []
         for name, attr in inspect.getmembers(EnvironmentVariables):
-            if name.startswith('_') or not hasattr(attr, 'name'):
+            if name.startswith(""_"") or not hasattr(attr, ""name""):
                 continue
             env_vars.append((name, attr))
         return env_vars
-    
+
     @classmethod
     def get_env_var_docstring(cls, name: str) -> Optional[str]:
         """"""Get the docstring for an environment variable.
-        
+
         Args:
             name: The name of the environment variable.
-            
+
         Returns:
             The docstring for the environment variable, or None if not found.
         """"""
         source_code = inspect.getsource(EnvironmentVariables)
         lines = source_code.splitlines()
-        
+
         for i, line in enumerate(lines):
             if f""{name}:"" in line and ""EnvVar"" in line:
                 j = i - 1
                 comments = []
-                while j >= 0 and lines[j].strip().startswith('#'):
+                while j >= 0 and lines[j].strip().startswith(""#""):
                     comments.insert(0, lines[j].strip()[1:].strip())
                     j -= 1
                 if comments:
                     return ""
"".join(comments)
         return None
-    
+
     @classmethod
     def generate_env_var_table(cls, include_internal: bool = False) -> rx.Component:
         """"""Generate a table of environment variables.
-        
+
         Args:
             include_internal: Whether to include internal environment variables.
-            
+
         Returns:
             A Reflex component containing the table.
         """"""
         env_vars = cls.get_all_env_vars()
-        
+
         if not include_internal:
-            env_vars = [(name, var) for name, var in env_vars if not getattr(var, 'internal', False)]
-        
+            env_vars = [
+                (name, var)
+                for name, var in env_vars
+                if not getattr(var, ""internal"", False)
+            ]
+
         env_vars.sort(key=lambda x: x[0])
-        
+
         return rx.box(
             rx.table.root(
                 rx.table.header(
                     rx.table.row(
-                        rx.table.column_header_cell(""Name"", class_name=""font-small text-slate-12 text-normal w-[20%] justify-start pl-4 font-bold""),
-                        rx.table.column_header_cell(""Type"", class_name=""font-small text-slate-12 text-normal w-[15%] justify-start pl-4 font-bold""),
-                        rx.table.column_header_cell(""Default"", class_name=""font-small text-slate-12 text-normal w-[15%] justify-start pl-4 font-bold""),
-                        rx.table.column_header_cell(""Description"", class_name=""font-small text-slate-12 text-normal w-[50%] justify-start pl-4 font-bold""),
+                        rx.table.column_header_cell(
+                            ""Name"",
+                            class_name=""font-small text-slate-12 text-normal w-[20%] justify-start pl-4 font-bold"",
+                        ),
+                        rx.table.column_header_cell(
+                            ""Type"",
+                            class_name=""font-small text-slate-12 text-normal w-[15%] justify-start pl-4 font-bold"",
+                        ),
+                        rx.table.column_header_cell(
+                            ""Default"",
+                            class_name=""font-small text-slate-12 text-normal w-[15%] justify-start pl-4 font-bold"",
+                        ),
+                        rx.table.column_header_cell(
+                            ""Description"",
+                            class_name=""font-small text-slate-12 text-normal w-[50%] justify-start pl-4 font-bold"",
+                        ),
                     )
                 ),
                 rx.table.body(
@@ -86,7 +103,14 @@ def generate_env_var_table(cls, include_internal: bool = False) -> rx.Component:
                                 class_name=""w-[20%]"",
                             ),
                             rx.table.cell(
-                                rx.code(str(var.type_.__name__ if hasattr(var.type_, ""__name__"") else str(var.type_)), class_name=""code-style""),
+                                rx.code(
+                                    str(
+                                        var.type_.__name__
+                                        if hasattr(var.type_, ""__name__"")
+                                        else str(var.type_)
+                                    ),
+                                    class_name=""code-style"",
+                                ),
                                 class_name=""w-[15%]"",
                             ),
                             rx.table.cell(
@@ -110,13 +134,15 @@ def generate_env_var_table(cls, include_internal: bool = False) -> rx.Component:
 
 def env_vars_page():
     """"""Generate the environment variables documentation page.
-    
+
     Returns:
         A Reflex component containing the documentation.
     """"""
     return rx.box(
         h1_comp(text=""Environment Variables""),
-        rx.code(""reflex.config.EnvironmentVariables"", class_name=""code-style text-[18px]""),
+        rx.code(
+            ""reflex.config.EnvironmentVariables"", class_name=""code-style text-[18px]""
+        ),
         rx.divider(),
         markdown(
             """"""
@@ -131,5 +157,9 @@ def env_vars_page():
     )
 
 
-env_vars_doc = docpage(""/docs/api-reference/environment-variables/"", ""Environment Variables"", right_sidebar=False)(env_vars_page)
+env_vars_doc = docpage(
+    ""/docs/api-reference/environment-variables/"",
+    ""Environment Variables"",
+    right_sidebar=False,
+)(env_vars_page)
 env_vars_doc.title = ""Environment Variables""