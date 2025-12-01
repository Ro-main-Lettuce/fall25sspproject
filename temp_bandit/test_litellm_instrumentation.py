@@ -4,9 +4,6 @@
 from unittest.mock import Mock, patch, MagicMock
 import sys
 
-# Mock litellm before importing our instrumentation
-sys.modules[""litellm""] = MagicMock()
-
 from agentops.instrumentation.providers.litellm import LiteLLMInstrumentor
 from agentops.instrumentation.providers.litellm.callback_handler import AgentOpsLiteLLMCallback
 from agentops.instrumentation.providers.litellm.utils import (
@@ -17,6 +14,9 @@
 )
 from agentops.instrumentation.providers.litellm.stream_wrapper import StreamWrapper, ChunkAggregator
 
+# Mock litellm before importing our instrumentation
+sys.modules[""litellm""] = MagicMock()
+
 
 class TestLiteLLMUtils(unittest.TestCase):
     """"""Test utility functions.""""""
@@ -70,7 +70,9 @@ def __next__(self):
     def test_parse_litellm_error(self):
         """"""Test error parsing.""""""
         # Mock LiteLLM error
-        error = Exception(""Rate limit exceeded"")
+        error = Mock(spec=Exception)
+        error.__class__.__name__ = ""Exception""
+        error.args = (""Rate limit exceeded"",)
         error.status_code = 429
         error.llm_provider = ""openai""
 