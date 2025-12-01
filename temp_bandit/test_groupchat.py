@@ -10,6 +10,7 @@
 import io
 import json
 import logging
+import tempfile
 from types import SimpleNamespace
 from typing import Any, Optional
 from unittest import mock
@@ -21,6 +22,8 @@
 from autogen.agentchat.contrib.capabilities import transform_messages, transforms
 from autogen.exception_utils import AgentNameConflict, UndefinedNextAgent
 
+from ..conftest import Credentials
+
 
 def test_func_call_groupchat():
     agent1 = autogen.ConversableAgent(
@@ -2181,6 +2184,51 @@ def test_manager_resume_message_assignment():
     assert list(agent_a.chat_messages.values())[0] == prev_messages[:-1]
 
 
+@pytest.mark.deepseek
+def test_groupchat_with_deepseek_reasoner(
+    credentials_gpt_4o_mini: Credentials,
+    credentials_deepseek_reasoner: Credentials,
+) -> None:
+    with tempfile.TemporaryDirectory() as tmp_dir:
+        user_proxy = autogen.UserProxyAgent(
+            ""user_proxy"",
+            human_input_mode=""NEVER"",
+            code_execution_config={""work_dir"": tmp_dir, ""use_docker"": False},
+        )
+
+        supervisor = autogen.AssistantAgent(
+            ""supervisor"",
+            llm_config={
+                ""config_list"": credentials_deepseek_reasoner.config_list,
+            },
+        )
+
+        assistant = autogen.AssistantAgent(
+            ""assistant"",
+            llm_config={
+                ""config_list"": credentials_deepseek_reasoner.config_list,
+            },
+        )
+
+        groupchat = autogen.GroupChat(
+            agents=[user_proxy, supervisor, assistant],
+            messages=[""A group chat""],
+            max_round=5,
+        )
+
+        manager = autogen.GroupChatManager(
+            groupchat=groupchat,
+            llm_config={
+                ""config_list"": credentials_gpt_4o_mini.config_list,
+            },
+        )
+
+        result = user_proxy.initiate_chat(
+            manager, message=""""""Give me some info about the stock market"""""", summary_method=""reflection_with_llm""
+        )
+        assert isinstance(result.summary, str)
+
+
 if __name__ == ""__main__"":
     # test_func_call_groupchat()
     # test_broadcast()