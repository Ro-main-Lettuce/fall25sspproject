@@ -15,7 +15,7 @@
 from ....utils import image
 
 
-class AnthropicMessages(requester.LLMAPIRequester):
+class AnthropicMessages(requester.ProviderAPIRequester):
     """"""Anthropic Messages API 请求器""""""
 
     client: anthropic.AsyncAnthropic