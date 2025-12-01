@@ -17,22 +17,20 @@
 from openai import AzureOpenAI, OpenAI
 from openai.types.chat import ChatCompletion
 
-from autogen.logger.base_logger import BaseLogger
-from autogen.logger.logger_utils import get_current_ts, to_dict
-
-from .base_logger import LLMConfig
+from .base_logger import BaseLogger, LLMConfig
+from .logger_utils import get_current_ts, to_dict
 
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
+    from .. import Agent, ConversableAgent, OpenAIWrapper
+    from ..oai.anthropic import AnthropicClient
+    from ..oai.bedrock import BedrockClient
+    from ..oai.cerebras import CerebrasClient
+    from ..oai.cohere import CohereClient
+    from ..oai.gemini import GeminiClient
+    from ..oai.groq import GroqClient
+    from ..oai.mistral import MistralAIClient
+    from ..oai.ollama import OllamaClient
+    from ..oai.together import TogetherClient
 
 logger = logging.getLogger(__name__)
 lock = threading.Lock()
@@ -309,7 +307,7 @@ def log_new_agent(self, agent: ConversableAgent, init_args: dict[str, Any]) -> N
             agent (ConversableAgent): Agent to log.
             init_args (dict[str, Any]): Initialization arguments of the agent
         """"""
-        from autogen import Agent
+        from .. import Agent
 
         if self.con is None:
             return