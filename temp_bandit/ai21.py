@@ -16,6 +16,8 @@
 class AI21Provider(InstrumentedProvider):
     original_create = None
     original_create_async = None
+    original_answer = None
+    original_answer_async = None
 
     def __init__(self, client):
         super().__init__(client)
@@ -27,6 +29,7 @@ def handle_response(self, response, kwargs, init_timestamp, session: Optional[Se
         from ai21.stream.async_stream import AsyncStream
         from ai21.models.chat.chat_completion_chunk import ChatCompletionChunk
         from ai21.models.chat.chat_completion_response import ChatCompletionResponse
+        from ai21.models.responses.answer_response import AnswerResponse
 
         llm_event = LLMEvent(init_timestamp=init_timestamp, params=kwargs)
         action_event = ActionEvent(init_timestamp=init_timestamp, params=kwargs)
@@ -45,7 +48,7 @@ def handle_stream_chunk(chunk: ChatCompletionChunk):
                 accumulated_delta = llm_event.returns.choices[0].delta
                 llm_event.agent_id = check_call_stack_for_agent_id()
                 llm_event.model = kwargs[""model""]
-                llm_event.prompt = [message if isinstance(message, dict) else message.model_dump() for message in kwargs[""messages""]]
+                llm_event.prompt = [message.model_dump() for message in kwargs[""messages""]]
 
                 # NOTE: We assume for completion only choices[0] is relevant
                 choice = chunk.choices[0]
@@ -109,14 +112,23 @@ async def async_generator():
                 llm_event.returns = response
                 llm_event.agent_id = check_call_stack_for_agent_id()
                 llm_event.model = kwargs[""model""]
-                llm_event.prompt = [message if isinstance(message, dict) else message.model_dump() for message in kwargs[""messages""]]
+                llm_event.prompt = [message.model_dump() for message in kwargs[""messages""]]
                 llm_event.prompt_tokens = response.usage.prompt_tokens
                 llm_event.completion = response.choices[0].message.model_dump()
                 llm_event.completion_tokens = response.usage.completion_tokens
                 llm_event.end_timestamp = get_ISO_time()
                 self._safe_record(session, llm_event)
 
-            # Chat completion response handling only
+            elif isinstance(response, AnswerResponse):
+                action_event.returns = response
+                action_event.agent_id = check_call_stack_for_agent_id()
+                action_event.action_type = ""Contextual Answers""
+                action_event.logs = [
+                    {""context"": kwargs[""context""], ""question"": kwargs[""question""]},
+                    response.model_dump() if response.model_dump() else None,
+                ]
+                action_event.end_timestamp = get_ISO_time()
+                self._safe_record(session, action_event)
 
         except Exception as e:
             self._safe_record(session, ErrorEvent(trigger_event=llm_event, exception=e))
@@ -133,6 +145,8 @@ async def async_generator():
     def override(self):
         self._override_completion()
         self._override_completion_async()
+        self._override_answer()
+        self._override_answer_async()
 
     def _override_completion(self):
         from ai21.clients.studio.resources.chat import ChatCompletions
@@ -170,17 +184,59 @@ async def patched_function(*args, **kwargs):
         # Override the original method with the patched one
         AsyncChatCompletions.create = patched_function
 
-    # Removed answer-related overrides as we're only using chat completions
+    def _override_answer(self):
+        from ai21.clients.studio.resources.studio_answer import StudioAnswer
+
+        global original_answer
+        original_answer = StudioAnswer.create
+
+        def patched_function(*args, **kwargs):
+            # Call the original function with its original arguments
+            init_timestamp = get_ISO_time()
+
+            session = kwargs.get(""session"", None)
+            if ""session"" in kwargs.keys():
+                del kwargs[""session""]
+            result = original_answer(*args, **kwargs)
+            return self.handle_response(result, kwargs, init_timestamp, session=session)
+
+        StudioAnswer.create = patched_function
+
+    def _override_answer_async(self):
+        from ai21.clients.studio.resources.studio_answer import AsyncStudioAnswer
+
+        global original_answer_async
+        original_answer_async = AsyncStudioAnswer.create
+
+        async def patched_function(*args, **kwargs):
+            # Call the original function with its original arguments
+            init_timestamp = get_ISO_time()
+
+            session = kwargs.get(""session"", None)
+            if ""session"" in kwargs.keys():
+                del kwargs[""session""]
+            result = await original_answer_async(*args, **kwargs)
+            return self.handle_response(result, kwargs, init_timestamp, session=session)
+
+        AsyncStudioAnswer.create = patched_function
 
     def undo_override(self):
         if (
             self.original_create is not None
             and self.original_create_async is not None
+            and self.original_answer is not None
+            and self.original_answer_async is not None
         ):
             from ai21.clients.studio.resources.chat import (
                 ChatCompletions,
                 AsyncChatCompletions,
             )
+            from ai21.clients.studio.resources.studio_answer import (
+                StudioAnswer,
+                AsyncStudioAnswer,
+            )
 
             ChatCompletions.create = self.original_create
             AsyncChatCompletions.create = self.original_create_async
+            StudioAnswer.create = self.original_answer
+            AsyncStudioAnswer.create = self.original_answer_async