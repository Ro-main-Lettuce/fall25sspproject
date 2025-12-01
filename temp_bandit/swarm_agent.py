@@ -12,9 +12,8 @@
 
 from pydantic import BaseModel
 
-from autogen.oai import OpenAIWrapper
-from autogen.tools import get_function_schema
-
+from ...oai import OpenAIWrapper
+from ...tools import get_function_schema
 from ..agent import Agent
 from ..chat import ChatResult
 from ..conversable_agent import ConversableAgent
@@ -223,7 +222,7 @@ def _process_initial_messages(
     temp_user_proxy = None
     temp_user_list = []
     if len(messages) == 1 and ""name"" not in messages[0] and not user_agent:
-        temp_user_proxy = UserProxyAgent(name=""_User"")
+        temp_user_proxy = UserProxyAgent(name=""_User"", code_execution_config=False)
         last_agent = temp_user_proxy
         temp_user_list.append(temp_user_proxy)
     else:
@@ -297,45 +296,54 @@ def _determine_next_agent(
     if ""tool_calls"" in groupchat.messages[-1]:
         return tool_execution
 
+    after_work_condition = None
+
     if tool_execution._next_agent is not None:
         next_agent = tool_execution._next_agent
         tool_execution._next_agent = None
 
-        # Check for string, access agent from group chat.
+        if not isinstance(next_agent, AfterWorkOption):
+            # Check for string, access agent from group chat.
 
-        if isinstance(next_agent, str):
-            if next_agent in swarm_agent_names:
-                next_agent = groupchat.agent_by_name(name=next_agent)
-            else:
-                raise ValueError(f""No agent found with the name '{next_agent}'. Ensure the agent exists in the swarm."")
+            if isinstance(next_agent, str):
+                if next_agent in swarm_agent_names:
+                    next_agent = groupchat.agent_by_name(name=next_agent)
+                else:
+                    raise ValueError(
+                        f""No agent found with the name '{next_agent}'. Ensure the agent exists in the swarm.""
+                    )
 
-        return next_agent
+            return next_agent
+        else:
+            after_work_condition = next_agent
 
     # get the last swarm agent
     last_swarm_speaker = None
     for message in reversed(groupchat.messages):
-        if ""name"" in message and message[""name""] in swarm_agent_names:
+        if ""name"" in message and message[""name""] in swarm_agent_names and message[""name""] != __TOOL_EXECUTOR_NAME__:
             agent = groupchat.agent_by_name(name=message[""name""])
             if isinstance(agent, SwarmAgent):
                 last_swarm_speaker = agent
                 break
     if last_swarm_speaker is None:
         raise ValueError(""No swarm agent found in the message history"")
 
-    # If the user last spoke, return to the agent prior
-    if (user_agent and last_speaker == user_agent) or groupchat.messages[-1][""role""] == ""tool"":
-        return last_swarm_speaker
+    if after_work_condition is None:
+        # If the user last spoke, return to the agent prior
+        if (user_agent and last_speaker == user_agent) or groupchat.messages[-1][""role""] == ""tool"":
+            return last_swarm_speaker
 
-    # Resolve after_work condition (agent-level overrides global)
-    after_work_condition = (
-        last_swarm_speaker.after_work if last_swarm_speaker.after_work is not None else swarm_after_work
-    )
-    if isinstance(after_work_condition, AFTER_WORK):
-        after_work_condition = after_work_condition.agent
+        # Resolve after_work condition (agent-level overrides global)
+        after_work_condition = (
+            last_swarm_speaker.after_work if last_swarm_speaker.after_work is not None else swarm_after_work
+        )
+
+        if isinstance(after_work_condition, AFTER_WORK):
+            after_work_condition = after_work_condition.agent
 
-    # Evaluate callable after_work
-    if isinstance(after_work_condition, Callable):
-        after_work_condition = after_work_condition(last_speaker, groupchat.messages, groupchat)
+        # Evaluate callable after_work
+        if isinstance(after_work_condition, Callable):
+            after_work_condition = after_work_condition(last_swarm_speaker, groupchat.messages, groupchat)
 
     if isinstance(after_work_condition, str):  # Agent name in a string
         if after_work_condition in swarm_agent_names:
@@ -350,7 +358,7 @@ def _determine_next_agent(
         elif after_work_condition == AfterWorkOption.REVERT_TO_USER:
             return None if user_agent is None else user_agent
         elif after_work_condition == AfterWorkOption.STAY:
-            return last_speaker
+            return last_swarm_speaker
         elif after_work_condition == AfterWorkOption.SWARM_MANAGER:
             return ""auto""
     else:
@@ -565,7 +573,7 @@ class SwarmResult(BaseModel):
     """"""
 
     values: str = """"
-    agent: Optional[Union[""SwarmAgent"", str]] = None
+    agent: Optional[Union[""SwarmAgent"", str, AfterWorkOption]] = None
     context_variables: dict[str, Any] = {}
 
     class Config:  # Add this inner class