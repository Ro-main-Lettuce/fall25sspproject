@@ -11,11 +11,11 @@
 from collections import defaultdict
 from typing import Any, Optional, Union
 
-from autogen import OpenAIWrapper
-from autogen.agentchat.agent import Agent
-from autogen.agentchat.assistant_agent import AssistantAgent, ConversableAgent
-from autogen.oai.openai_utils import create_gpt_assistant, retrieve_assistants_by_name, update_gpt_assistant
-from autogen.runtime_logging import log_new_agent, logging_enabled
+from ... import OpenAIWrapper
+from ...oai.openai_utils import create_gpt_assistant, retrieve_assistants_by_name, update_gpt_assistant
+from ...runtime_logging import log_new_agent, logging_enabled
+from ..agent import Agent
+from ..assistant_agent import AssistantAgent, ConversableAgent
 
 logger = logging.getLogger(__name__)
 