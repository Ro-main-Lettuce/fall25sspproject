@@ -1,9 +1,7 @@
 import pytest
 
 from bespokelabs.curator.request_processor.config import OnlineRequestProcessorConfig
-from bespokelabs.curator.request_processor.online.openai_online_request_processor import (
-    OpenAIOnlineRequestProcessor,
-)
+from bespokelabs.curator.request_processor.online.openai_online_request_processor import OpenAIOnlineRequestProcessor
 
 
 def test_special_token_handling():