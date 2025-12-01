@@ -3,6 +3,7 @@
 from autogen import LLMConfig
 from autogen.agentchat import AssistantAgent as AutoGenAssistantAgent
 from autogen.agentchat import ConversableAgent as AutoGenConversableAgent
+from autogen.agentchat import ChatResult
 from autogen.agentchat.contrib.web_surfer import WebSurferAgent as AutoGenWebSurferAgent
 from pydantic import BaseModel, Field, HttpUrl
 
@@ -140,8 +141,8 @@ def is_termination_msg(self, msg: dict[str, Any]) -> bool:
             self.last_is_termination_msg_error = str(e)
             return False
 
-    def _get_error_message(self, run_response: Any) -> Optional[str]:
-        messages = [msg[""content""] for msg in run_response.messages]
+    def _get_error_message(self, chat_result: ChatResult) -> Optional[str]:
+        messages = [msg[""content""] for msg in chat_result.chat_history]
         last_message = messages[-1]
         if ""TERMINATE"" in last_message:
             return self.error_message
@@ -153,8 +154,8 @@ def _get_error_message(self, run_response: Any) -> Optional[str]:
 
         return None
 
-    def _get_answer(self, run_response: Any) -> WebSurferAnswer:
-        messages = [msg[""content""] for msg in run_response.messages]
+    def _get_answer(self, chat_result: ChatResult) -> WebSurferAnswer:
+        messages = [msg[""content""] for msg in chat_result.chat_history]
         last_message = messages[-1]
         return WebSurferAnswer.model_validate_json(last_message)
 
@@ -164,15 +165,15 @@ def _chat_with_websurfer(
         msg: Optional[str] = message
 
         while msg is not None:
-            run_response = self.websurfer.run(
+            chat_result = self.websurfer.initiate_chat(
                 self.assistant,
                 clear_history=clear_history,
                 message=msg,
             )
-            msg = self._get_error_message(run_response)
+            msg = self._get_error_message(chat_result)
             clear_history = False
 
-        return self._get_answer(run_response)
+        return self._get_answer(chat_result)
 
     def _get_error_from_exception(self, task: str, e: Exception) -> str:
         answer = WebSurferAnswer(