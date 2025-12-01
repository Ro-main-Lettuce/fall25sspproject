@@ -8,10 +8,8 @@
 
 from termcolor import colored
 
-import autogen
-from autogen import UserProxyAgent
-from autogen.agentchat.conversable_agent import ConversableAgent
-
+from .... import GroupChat, GroupChatManager, UserProxyAgent
+from ...conversable_agent import ConversableAgent
 from .agent_builder import AgentBuilder
 from .tool_retriever import ToolBuilder, format_ag2_tool, get_full_tool_description
 
@@ -465,13 +463,13 @@ def _run_autobuild(self, group_name: str, execution_task: str, building_task: st
 
         self.build_times += 1
         # start nested chat
-        nested_group_chat = autogen.GroupChat(
+        nested_group_chat = GroupChat(
             agents=agent_list,
             messages=[],
             allow_repeat_speaker=agent_list[:-1] if agent_configs[""coding""] is True else agent_list,
             **self._nested_config[""group_chat_config""],
         )
-        manager = autogen.GroupChatManager(
+        manager = GroupChatManager(
             groupchat=nested_group_chat,
             llm_config=self._nested_config[""group_chat_llm_config""],
         )