@@ -12,6 +12,11 @@
 - get_config_spec: Get connector configuration schema
 - validate_config: Validate config and detect hardcoded secrets
 - run_sync: Execute sync operations to DuckDB cache
+- create_stream_template: Create or modify stream templates for manifest-only connectors
+- create_auth_logic: Create or modify authentication logic for streams
+- test_auth_logic: Test authentication without hitting endpoints
+- create_stream_from_template: Create new streams from existing templates
+- test_stream_read: Test stream reads using CDK test-read functionality
 
 For production use, the MCP server would typically be started as a separate process
 and accessed by MCP clients (like AI assistants) via the stdio transport.
@@ -104,6 +109,13 @@ async def main() -> None:
 
     print(""
To use the MCP server with an MCP client:"")
     print(""python examples/run_mcp_server.py"")
+    
+    print(""
Example usage with mcp-cli:"")
+    print(""mcp-cli call pyairbyte list_connectors '{}'"")
+    print(""mcp-cli call pyairbyte create_stream_template '{\""connector_name\"": \""my-connector\"", \""stream_name\"": \""users\"", \""url_base\"": \""https://api.example.com\"", \""path\"": \""/users\""}'"")
+    
+    print(""
For manifest-only connector development:"")
+    print(""python examples/test_mcp_manifest_actions.py"")
 
 
 if __name__ == ""__main__"":