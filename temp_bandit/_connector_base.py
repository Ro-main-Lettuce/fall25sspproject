@@ -348,7 +348,7 @@ def check(self) -> None:
     def install(self) -> None:
         """"""Install the connector if it is not yet installed.""""""
         self.executor.install()
-        rich.print(""For configuration instructions, see: 
"" f""{self.docs_url}#reference
"")
+        rich.print(f""For configuration instructions, see: 
{self.docs_url}#reference
"")
 
     def uninstall(self) -> None:
         """"""Uninstall the connector if it is installed.