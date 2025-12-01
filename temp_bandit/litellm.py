@@ -51,27 +51,18 @@ def handle_response(self, response, kwargs, init_timestamp, session: Optional[Se
         if session is not None:
             llm_event.session_id = session.session_id
 
-        def handle_stream_chunk(chunk):
+        def handle_stream_chunk(chunk: ChatCompletionChunk):
             # NOTE: prompt/completion usage not returned in response when streaming
             # We take the first ChatCompletionChunk and accumulate the deltas from all subsequent chunks to build one full chat completion
-            if llm_event.returns is None:
-                if isinstance(chunk, str):
-                    llm_event.returns = {""choices"": [{""delta"": {""content"": """", ""role"": ""assistant""}}]}
-                else:
-                    llm_event.returns = chunk.model_dump() if hasattr(chunk, 'model_dump') else chunk
+            if llm_event.returns == None:
+                llm_event.returns = chunk
 
             try:
-                if isinstance(chunk, str):
-                    # Handle raw string chunks
-                    llm_event.returns.choices[0].delta.content += chunk
-                    return
-
                 accumulated_delta = llm_event.returns.choices[0].delta
                 llm_event.agent_id = check_call_stack_for_agent_id()
                 llm_event.model = chunk.model
                 llm_event.prompt = kwargs[""messages""]
 
-
                 # NOTE: We assume for completion only choices[0] is relevant
                 choice = chunk.choices[0]
 
@@ -181,24 +172,27 @@ def _override_completion(self):
         )  # Note: litellm calls all LLM APIs using the OpenAI format
         from openai.resources.chat import completions
 
-        original_create = litellm.completion  # Store locally to prevent recursion
+        self.original_create = litellm.completion
         self.original_oai_create = completions.Completions.create
 
         def patched_function(*args, **kwargs):
             init_timestamp = get_ISO_time()
 
-            session = kwargs.pop(""session"", None) if ""session"" in kwargs else None
+            session = kwargs.get(""session"", None)
+            if ""session"" in kwargs.keys():
+                del kwargs[""session""]
 
-            try:
-                completion_override = fetch_completion_override_from_time_travel_cache(kwargs)
-                if completion_override:
-                    result_model = ChatCompletion.model_validate_json(completion_override)
-                    return self.handle_response(result_model, kwargs, init_timestamp, session=session)
-            except RecursionError:
-                pass  # Skip time travel cache on recursion error
+            completion_override = fetch_completion_override_from_time_travel_cache(kwargs)
+            if completion_override:
+                result_model = ChatCompletion.model_validate_json(completion_override)
+                return self.handle_response(result_model, kwargs, init_timestamp, session=session)
+
+            # prompt_override = fetch_prompt_override_from_time_travel_cache(kwargs)
+            # if prompt_override:
+            #     kwargs[""messages""] = prompt_override[""messages""]
 
             # Call the original function with its original arguments
-            result = original_create(*args, **kwargs)
+            result = self.original_create(*args, **kwargs)
             return self.handle_response(result, kwargs, init_timestamp, session=session)
 
         litellm.completion = patched_function
@@ -210,23 +204,28 @@ def _override_async_completion(self):
         )  # Note: litellm calls all LLM APIs using the OpenAI format
         from openai.resources.chat import completions
 
-        original_create_async = litellm.acompletion  # Store locally to prevent recursion
+        self.original_create_async = litellm.acompletion
         self.original_oai_create_async = completions.AsyncCompletions.create
 
         async def patched_function(*args, **kwargs):
             init_timestamp = get_ISO_time()
-            session = kwargs.pop(""session"", None) if ""session"" in kwargs else None
 
-            try:
-                completion_override = fetch_completion_override_from_time_travel_cache(kwargs)
-                if completion_override:
-                    result_model = ChatCompletion.model_validate_json(completion_override)
-                    return self.handle_response(result_model, kwargs, init_timestamp, session=session)
-            except RecursionError:
-                pass  # Skip time travel cache on recursion error
+            session = kwargs.get(""session"", None)
+            if ""session"" in kwargs.keys():
+                del kwargs[""session""]
+
+            completion_override = fetch_completion_override_from_time_travel_cache(kwargs)
+            if completion_override:
+                result_model = ChatCompletion.model_validate_json(completion_override)
+                return self.handle_response(result_model, kwargs, init_timestamp, session=session)
+
+            # prompt_override = fetch_prompt_override_from_time_travel_cache(kwargs)
+            # if prompt_override:
+            #     kwargs[""messages""] = prompt_override[""messages""]
 
             # Call the original function with its original arguments
-            result = await original_create_async(*args, **kwargs)
+            result = await self.original_create_async(*args, **kwargs)
             return self.handle_response(result, kwargs, init_timestamp, session=session)
 
+        # Override the original method with the patched one
         litellm.acompletion = patched_function