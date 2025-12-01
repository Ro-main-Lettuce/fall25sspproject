@@ -6,12 +6,12 @@
 # SPDX-License-Identifier: MIT
 from typing import Literal, Optional, Union
 
-import autogen
-from autogen.agentchat.contrib.agent_eval.criterion import Criterion
-from autogen.agentchat.contrib.agent_eval.critic_agent import CriticAgent
-from autogen.agentchat.contrib.agent_eval.quantifier_agent import QuantifierAgent
-from autogen.agentchat.contrib.agent_eval.subcritic_agent import SubCriticAgent
-from autogen.agentchat.contrib.agent_eval.task import Task
+from .... import GroupChat, GroupChatManager, UserProxyAgent
+from .criterion import Criterion
+from .critic_agent import CriticAgent
+from .quantifier_agent import QuantifierAgent
+from .subcritic_agent import SubCriticAgent
+from .task import Task
 
 
 def generate_criteria(
@@ -38,7 +38,7 @@ def generate_criteria(
         llm_config=llm_config,
     )
 
-    critic_user = autogen.UserProxyAgent(
+    critic_user = UserProxyAgent(
         name=""critic_user"",
         max_consecutive_auto_reply=0,  # terminate without auto-reply
         human_input_mode=""NEVER"",
@@ -53,10 +53,8 @@ def generate_criteria(
         )
         agents.append(subcritic)
 
-    groupchat = autogen.GroupChat(
-        agents=agents, messages=[], max_round=max_round, speaker_selection_method=""round_robin""
-    )
-    critic_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
+    groupchat = GroupChat(agents=agents, messages=[], max_round=max_round, speaker_selection_method=""round_robin"")
+    critic_manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
 
     critic_user.initiate_chat(critic_manager, message=task.get_sys_message())
     criteria = critic_user.last_message()
@@ -90,7 +88,7 @@ def quantify_criteria(
         llm_config=llm_config,
     )
 
-    quantifier_user = autogen.UserProxyAgent(
+    quantifier_user = UserProxyAgent(
         name=""quantifier_user"",
         max_consecutive_auto_reply=0,  # terminate without auto-reply
         human_input_mode=""NEVER"",