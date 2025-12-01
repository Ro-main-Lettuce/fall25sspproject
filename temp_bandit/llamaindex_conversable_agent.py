@@ -6,19 +6,21 @@
 # SPDX-License-Identifier: MIT
 from typing import Optional, Union
 
-from autogen import OpenAIWrapper
-from autogen.agentchat import Agent, ConversableAgent
-from autogen.agentchat.contrib.vectordb.utils import get_logger
+from ... import OpenAIWrapper
+from ...import_utils import optional_import_block, require_optional_import
+from .. import Agent, ConversableAgent
+from .vectordb.utils import get_logger
 
 logger = get_logger(__name__)
 
-try:
+with optional_import_block() as result:
     from llama_index.core.agent.runner.base import AgentRunner
     from llama_index.core.base.llms.types import ChatMessage
     from llama_index.core.chat_engine.types import AgentChatResponse
     from pydantic import BaseModel
     from pydantic import __version__ as pydantic_version
 
+if result.is_successful:
     # let's Avoid: AttributeError: type object 'Config' has no attribute 'copy'
     # check for v1 like in autogen/_pydantic.py
     is_pydantic_v1 = pydantic_version.startswith(""1."")
@@ -35,16 +37,13 @@ class Config:
     # Added to mitigate PydanticSchemaGenerationError
     BaseModel.model_config = Config
 
-except ImportError as e:
-    logger.fatal(""Failed to import llama-index. Try running 'pip install llama-index'"")
-    raise e
-
 
+@require_optional_import(""llama_index"", ""neo4j"")
 class LLamaIndexConversableAgent(ConversableAgent):
     def __init__(
         self,
         name: str,
-        llama_index_agent: AgentRunner,
+        llama_index_agent: ""AgentRunner"",
         description: Optional[str] = None,
         **kwargs,
     ):
@@ -85,7 +84,7 @@ def _generate_oai_reply(
         """"""Generate a reply using autogen.oai.""""""
         user_message, history = self._extract_message_and_history(messages=messages, sender=sender)
 
-        chat_response: AgentChatResponse = self._llama_index_agent.chat(message=user_message, chat_history=history)
+        chat_response: ""AgentChatResponse"" = self._llama_index_agent.chat(message=user_message, chat_history=history)
 
         extracted_response = chat_response.response
 
@@ -100,7 +99,7 @@ async def _a_generate_oai_reply(
         """"""Generate a reply using autogen.oai.""""""
         user_message, history = self._extract_message_and_history(messages=messages, sender=sender)
 
-        chat_response: AgentChatResponse = await self._llama_index_agent.achat(
+        chat_response: ""AgentChatResponse"" = await self._llama_index_agent.achat(
             message=user_message, chat_history=history
         )
 
@@ -110,7 +109,7 @@ async def _a_generate_oai_reply(
 
     def _extract_message_and_history(
         self, messages: Optional[list[dict]] = None, sender: Optional[Agent] = None
-    ) -> tuple[str, list[ChatMessage]]:
+    ) -> tuple[str, list[""ChatMessage""]]:
         """"""Extract the message and history from the messages.""""""
         if not messages:
             messages = self._oai_messages[sender]
@@ -121,7 +120,7 @@ def _extract_message_and_history(
         message = messages[-1].get(""content"", """")
 
         history = messages[:-1]
-        history_messages: list[ChatMessage] = []
+        history_messages: list[""ChatMessage""] = []
         for history_message in history:
             content = history_message.get(""content"", """")
             role = history_message.get(""role"", ""user"")