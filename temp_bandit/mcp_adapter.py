@@ -87,22 +87,9 @@ def __init__(
         self._tool_names = list(tool_names) if tool_names else None
 
         if not MCP_AVAILABLE:
-            import click
-
-            if click.confirm(
-                ""You are missing the 'mcp' package. Would you like to install it?""
-            ):
-                import subprocess
-
-                try:
-                    subprocess.run([""uv"", ""add"", ""mcp crewai-tools[mcp]""], check=True)
-
-                except subprocess.CalledProcessError:
-                    raise ImportError(""Failed to install mcp package"")
-            else:
-                raise ImportError(
-                    ""`mcp` package not found, please run `uv add crewai-tools[mcp]`""
-                )
+            raise ImportError(
+                ""`mcp` package not found, please run `uv add crewai-tools[mcp]`""
+            )
 
         try:
             self._serverparams = serverparams