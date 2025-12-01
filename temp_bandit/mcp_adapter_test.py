@@ -1,11 +1,19 @@
 from textwrap import dedent
 
 import pytest
-from mcp import StdioServerParameters
 
 from crewai_tools import MCPServerAdapter
 from crewai_tools.adapters.tool_collection import ToolCollection
 
+try:
+    from mcp import StdioServerParameters
+    MCP_AVAILABLE = True
+except ImportError:
+    MCP_AVAILABLE = False
+    class StdioServerParameters:
+        def __init__(self, **kwargs):
+            pass
+
 @pytest.fixture
 def echo_server_script():
     return dedent(
@@ -73,6 +81,7 @@ def echo_sse_server(echo_server_sse_script):
         process.wait()
 
 
+@pytest.mark.skipif(not MCP_AVAILABLE, reason=""mcp package not available"")
 def test_context_manager_syntax(echo_server_script):
     serverparams = StdioServerParameters(
         command=""uv"", args=[""run"", ""python"", ""-c"", echo_server_script]
@@ -85,6 +94,7 @@ def test_context_manager_syntax(echo_server_script):
         assert tools[0].run(text=""hello"") == ""Echo: hello""
         assert tools[1].run(a=5, b=3) == '8'
 
+@pytest.mark.skipif(not MCP_AVAILABLE, reason=""mcp package not available"")
 def test_context_manager_syntax_sse(echo_sse_server):
     sse_serverparams = echo_sse_server
     with MCPServerAdapter(sse_serverparams) as tools:
@@ -94,6 +104,7 @@ def test_context_manager_syntax_sse(echo_sse_server):
         assert tools[0].run(text=""hello"") == ""Echo: hello""
         assert tools[1].run(a=5, b=3) == '8'
 
+@pytest.mark.skipif(not MCP_AVAILABLE, reason=""mcp package not available"")
 def test_try_finally_syntax(echo_server_script):
     serverparams = StdioServerParameters(
         command=""uv"", args=[""run"", ""python"", ""-c"", echo_server_script]
@@ -109,6 +120,7 @@ def test_try_finally_syntax(echo_server_script):
     finally:
         mcp_server_adapter.stop()
 
+@pytest.mark.skipif(not MCP_AVAILABLE, reason=""mcp package not available"")
 def test_try_finally_syntax_sse(echo_sse_server):
     sse_serverparams = echo_sse_server
     mcp_server_adapter = MCPServerAdapter(sse_serverparams)
@@ -122,6 +134,7 @@ def test_try_finally_syntax_sse(echo_sse_server):
     finally:
         mcp_server_adapter.stop()
 
+@pytest.mark.skipif(not MCP_AVAILABLE, reason=""mcp package not available"")
 def test_context_manager_with_filtered_tools(echo_server_script):
     serverparams = StdioServerParameters(
         command=""uv"", args=[""run"", ""python"", ""-c"", echo_server_script]
@@ -138,6 +151,7 @@ def test_context_manager_with_filtered_tools(echo_server_script):
         with pytest.raises(KeyError):
             _ = tools[""calc_tool""]
 
+@pytest.mark.skipif(not MCP_AVAILABLE, reason=""mcp package not available"")
 def test_context_manager_sse_with_filtered_tools(echo_sse_server):
     sse_serverparams = echo_sse_server
     # Only select the calc_tool
@@ -152,6 +166,7 @@ def test_context_manager_sse_with_filtered_tools(echo_sse_server):
         with pytest.raises(KeyError):
             _ = tools[""echo_tool""]
 
+@pytest.mark.skipif(not MCP_AVAILABLE, reason=""mcp package not available"")
 def test_try_finally_with_filtered_tools(echo_server_script):
     serverparams = StdioServerParameters(
         command=""uv"", args=[""run"", ""python"", ""-c"", echo_server_script]
@@ -168,6 +183,7 @@ def test_try_finally_with_filtered_tools(echo_server_script):
     finally:
         mcp_server_adapter.stop()
 
+@pytest.mark.skipif(not MCP_AVAILABLE, reason=""mcp package not available"")
 def test_filter_with_nonexistent_tool(echo_server_script):
     serverparams = StdioServerParameters(
         command=""uv"", args=[""run"", ""python"", ""-c"", echo_server_script]
@@ -178,6 +194,7 @@ def test_filter_with_nonexistent_tool(echo_server_script):
         assert len(tools) == 1
         assert tools[0].name == ""echo_tool""
 
+@pytest.mark.skipif(not MCP_AVAILABLE, reason=""mcp package not available"")
 def test_filter_with_only_nonexistent_tools(echo_server_script):
     serverparams = StdioServerParameters(
         command=""uv"", args=[""run"", ""python"", ""-c"", echo_server_script]
@@ -187,3 +204,22 @@ def test_filter_with_only_nonexistent_tools(echo_server_script):
         # Should return an empty tool collection
         assert isinstance(tools, ToolCollection)
         assert len(tools) == 0
+
+
+def test_mcp_adapter_missing_dependency():
+    """"""Test that MCPServerAdapter raises ImportError when mcp package is missing.""""""
+    from unittest.mock import patch
+    
+    with patch('crewai_tools.adapters.mcp_adapter.MCP_AVAILABLE', False):
+        with pytest.raises(ImportError, match=""`mcp` package not found, please run `uv add crewai-tools\\[mcp\\]`""):
+            MCPServerAdapter({""url"": ""http://localhost:8000/sse""})
+
+
+def test_mcp_adapter_missing_dependency_stdio():
+    """"""Test that MCPServerAdapter raises ImportError for stdio params when mcp package is missing.""""""
+    from unittest.mock import patch, MagicMock
+    
+    with patch('crewai_tools.adapters.mcp_adapter.MCP_AVAILABLE', False):
+        mock_params = MagicMock()
+        with pytest.raises(ImportError, match=""`mcp` package not found, please run `uv add crewai-tools\\[mcp\\]`""):
+            MCPServerAdapter(mock_params)