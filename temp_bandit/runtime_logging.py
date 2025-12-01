@@ -9,25 +9,25 @@
 import logging
 import sqlite3
 import uuid
-from typing import TYPE_CHECKING, Any, Callable, Literal, TypeVar
+from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, TypeVar
 
 from openai import AzureOpenAI, OpenAI
 from openai.types.chat import ChatCompletion
 
-from autogen.logger.base_logger import BaseLogger, LLMConfig
-from autogen.logger.logger_factory import LoggerFactory
+from .logger.base_logger import BaseLogger, LLMConfig
+from .logger.logger_factory import LoggerFactory
 
 if TYPE_CHECKING:
-    from autogen import Agent, ConversableAgent, OpenAIWrapper
-    from autogen.oai.anthropic import AnthropicClient
-    from autogen.oai.bedrock import BedrockClient
-    from autogen.oai.cerebras import CerebrasClient
-    from autogen.oai.cohere import CohereClient
-    from autogen.oai.gemini import GeminiClient
-    from autogen.oai.groq import GroqClient
-    from autogen.oai.mistral import MistralAIClient
-    from autogen.oai.ollama import OllamaClient
-    from autogen.oai.together import TogetherClient
+    from . import Agent, ConversableAgent, OpenAIWrapper
+    from .oai.anthropic import AnthropicClient
+    from .oai.bedrock import BedrockClient
+    from .oai.cerebras import CerebrasClient
+    from .oai.cohere import CohereClient
+    from .oai.gemini import GeminiClient
+    from .oai.groq import GroqClient
+    from .oai.mistral import MistralAIClient
+    from .oai.ollama import OllamaClient
+    from .oai.together import TogetherClient
 
 logger = logging.getLogger(__name__)
 
@@ -38,9 +38,9 @@
 
 
 def start(
-    logger: BaseLogger | None = None,
+    logger: Optional[BaseLogger] = None,
     logger_type: Literal[""sqlite"", ""file""] = ""sqlite"",
-    config: dict[str, Any] | None = None,
+    config: Optional[dict[str, Any]] = None,
 ) -> str:
     """"""Start logging for the runtime.
 