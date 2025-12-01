@@ -3,6 +3,7 @@
 from dotenv import load_dotenv
 from openai import AsyncOpenAI, OpenAI
 import json, requests, time
+import aiohttp
 
 from bolna.constants import CHECKING_THE_DOCUMENTS_FILLER, DEFAULT_LANGUAGE_CODE
 from bolna.helpers.utils import convert_to_request_log, compute_function_pre_call_message
@@ -14,6 +15,9 @@
     
 
 class OpenAiLLM(BaseLLM):
+    _client_cache = {}
+    _client_lock = asyncio.Lock()
+    
     def __init__(self, max_tokens=100, buffer_size=40, model=""gpt-3.5-turbo-16k"", temperature=0.1, language=DEFAULT_LANGUAGE_CODE, **kwargs):
         super().__init__(max_tokens, buffer_size)
         self.model = model
@@ -30,31 +34,63 @@ def __init__(self, max_tokens=100, buffer_size=40, model=""gpt-3.5-turbo-16k"", te
             self.trigger_function_call = False
 
         self.started_streaming = False
-        logger.info(f""Initializing OpenAI LLM with model: {self.model} and maxc tokens {max_tokens}"")
+        logger.info(f""Initializing OpenAI LLM with model: {self.model} and max tokens {max_tokens}"")
         self.max_tokens = max_tokens
         self.temperature = temperature
         self.model_args = {""max_tokens"": self.max_tokens, ""temperature"": self.temperature, ""model"": self.model}
 
-        if kwargs.get(""provider"", ""openai"") == ""custom"":
-            base_url = kwargs.get(""base_url"")
-            api_key = kwargs.get('llm_key', None)
-            self.async_client = AsyncOpenAI(base_url=base_url, api_key= api_key)
-        else:
-            llm_key = kwargs.get('llm_key', os.getenv('OPENAI_API_KEY'))
-            self.async_client = AsyncOpenAI(api_key=llm_key)
-            api_key = llm_key
+        self.provider_type = kwargs.get(""provider"", ""openai"")
+        self.base_url = kwargs.get(""base_url"")
+        self.api_key = kwargs.get('llm_key', os.getenv('OPENAI_API_KEY'))
+        
+        self.client_key = f""{self.provider_type}:{self.base_url or 'default'}:{hash(self.api_key)}""
+        
+        logger.info(f""Initialized OpenAI LLM with connection pooling"")
+        logger.debug(f""Client key: {self.client_key}"")
+        
+        self.async_client = None
+        
         self.assistant_id = kwargs.get(""assistant_id"", None)
         if self.assistant_id:
             logger.info(f""Initializing OpenAI assistant with assistant id {self.assistant_id}"")
-            self.openai = OpenAI(api_key=api_key)
-            #self.thread_id = self.openai.beta.threads.create().id
+            self.openai = OpenAI(api_key=self.api_key)
             self.model_args = {""max_completion_tokens"": self.max_tokens, ""temperature"": self.temperature}
             my_assistant = self.openai.beta.assistants.retrieve(self.assistant_id)
             if my_assistant.tools is not None:
                 self.tools = [i for i in my_assistant.tools if i.type == ""function""]
-            #logger.info(f'thread id : {self.thread_id}')
+        
         self.run_id = kwargs.get(""run_id"", None)
         self.gave_out_prefunction_call_message = False
+    
+    async def _get_pooled_client(self) -> AsyncOpenAI:
+        """"""Get or create a pooled AsyncOpenAI client""""""
+        async with self._client_lock:
+            if self.client_key not in self._client_cache:
+                session = await self.get_pooled_session(""openai"")
+                
+                if self.provider_type == ""custom"" and self.base_url:
+                    client = AsyncOpenAI(
+                        base_url=self.base_url, 
+                        api_key=self.api_key
+                    )
+                else:
+                    client = AsyncOpenAI(
+                        api_key=self.api_key
+                    )
+                
+                try:
+                    if hasattr(client, '_client') and hasattr(client._client, '_session'):
+                        client._client._session = session
+                    logger.info(f""Successfully configured pooled session for OpenAI client"")
+                except Exception as e:
+                    logger.warning(f""Could not configure pooled session for OpenAI client: {e}"")
+                    logger.info(""OpenAI client will use default connection handling"")
+                
+                self._client_cache[self.client_key] = client
+                logger.info(f""Created pooled OpenAI client"")
+                logger.debug(f""Client key: {self.client_key}"")
+            
+            return self._client_cache[self.client_key]
 
     async def generate_stream(self, messages, synthesize=True, request_json=False, meta_info=None):
         if not messages or len(messages) == 0:
@@ -67,7 +103,7 @@ async def generate_stream(self, messages, synthesize=True, request_json=False, m
             ""messages"": messages,
             ""stream"": True,
             ""stop"": [""User:""],
-            ""user"": f""{self.run_id}#{meta_info['turn_id']}""
+            ""user"": f""{self.run_id}#{meta_info.get('turn_id', 'unknown') if meta_info else 'unknown'}""
         }
 
         if self.trigger_function_call:
@@ -87,6 +123,9 @@ async def generate_stream(self, messages, synthesize=True, request_json=False, m
         first_token_time = None
         latency_data = None
 
+        if not self.async_client:
+            self.async_client = await self._get_pooled_client()
+        
         async for chunk in await self.async_client.chat.completions.create(**model_args):
             now = time.time()
             if not first_token_time:
@@ -95,7 +134,7 @@ async def generate_stream(self, messages, synthesize=True, request_json=False, m
                 self.started_streaming = True
 
                 latency_data = {
-                    ""turn_id"": meta_info.get(""turn_id""),
+                    ""turn_id"": meta_info.get(""turn_id"") if meta_info else None,
                     ""model"": self.model,
                     ""first_token_latency_ms"": round(latency * 1000),
                     ""total_stream_duration_ms"": None  # Will be filled at end
@@ -190,6 +229,9 @@ async def generate_stream(self, messages, synthesize=True, request_json=False, m
     async def generate(self, messages, request_json=False):
         response_format = self.get_response_format(request_json)
 
+        if not self.async_client:
+            self.async_client = await self._get_pooled_client()
+            
         completion = await self.async_client.chat.completions.create(model=self.model, temperature=0.0, messages=messages,
                                                                      stream=False, response_format=response_format)
         res = completion.choices[0].message.content
@@ -199,4 +241,4 @@ def get_response_format(self, is_json_format: bool):
         if is_json_format and self.model in ('gpt-4-1106-preview', 'gpt-3.5-turbo-1106', 'gpt-4o-mini'):
             return {""type"": ""json_object""}
         else:
-            return {""type"": ""text""}
\ No newline at end of file
+            return {""type"": ""text""}