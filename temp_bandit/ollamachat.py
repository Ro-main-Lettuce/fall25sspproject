@@ -17,7 +17,7 @@
 REQUESTER_NAME: str = 'ollama-chat'
 
 
-class OllamaChatCompletions(requester.LLMAPIRequester):
+class OllamaChatCompletions(requester.ProviderAPIRequester):
     """"""Ollama平台 ChatCompletion API请求器""""""
 
     client: ollama.AsyncClient