@@ -84,7 +84,6 @@ async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
 async def main() -> None:
     """"""Main entry point for the MCP text editor server.""""""
     import argparse
-    import sys
 
     parser = argparse.ArgumentParser(description=""MCP Text Editor Server"")
     parser.add_argument(