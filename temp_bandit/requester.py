@@ -20,45 +20,45 @@ class RuntimeLLMModel:
     token_mgr: token.TokenManager
     """"""api key管理器""""""
 
-    requester: LLMAPIRequester
+    requester: ProviderAPIRequester
     """"""请求器实例""""""
 
     def __init__(
         self,
         model_entity: persistence_model.LLMModel,
         token_mgr: token.TokenManager,
-        requester: LLMAPIRequester,
+        requester: ProviderAPIRequester,
     ):
         self.model_entity = model_entity
         self.token_mgr = token_mgr
         self.requester = requester
 
 
-class RuntimeEmbeddingsModel:
-    """"""运行时 Embeddings 模型""""""
+class RuntimeEmbeddingModel:
+    """"""运行时 Embedding 模型""""""
 
-    model_entity: persistence_model.EmbeddingsModel
+    model_entity: persistence_model.EmbeddingModel
     """"""模型数据""""""
 
     token_mgr: token.TokenManager
     """"""api key管理器""""""
 
-    requester: LLMAPIRequester
+    requester: ProviderAPIRequester
     """"""请求器实例""""""
 
     def __init__(
         self,
-        model_entity: persistence_model.EmbeddingsModel,
+        model_entity: persistence_model.EmbeddingModel,
         token_mgr: token.TokenManager,
-        requester: LLMAPIRequester,
+        requester: ProviderAPIRequester,
     ):
         self.model_entity = model_entity
         self.token_mgr = token_mgr
         self.requester = requester
 
 
-class LLMAPIRequester(metaclass=abc.ABCMeta):
-    """"""LLM API请求器""""""
+class ProviderAPIRequester(metaclass=abc.ABCMeta):
+    """"""Provider API请求器""""""
 
     name: str = None
 
@@ -97,19 +97,19 @@ async def invoke_llm(
             llm_entities.Message: 返回消息对象
         """"""
         pass
-        
-    async def invoke_embeddings(
+
+    async def invoke_embedding(
         self,
         query: core_entities.Query,
-        model: RuntimeEmbeddingsModel,
+        model: RuntimeEmbeddingModel,
         input_text: str,
         extra_args: dict[str, typing.Any] = {},
     ) -> list[float]:
-        """"""调用 Embeddings API
+        """"""调用 Embedding API
 
         Args:
             query (core_entities.Query): 请求上下文
-            model (RuntimeEmbeddingsModel): 使用的模型信息
+            model (RuntimeEmbeddingModel): 使用的模型信息
             input_text (str): 输入文本
             extra_args (dict[str, typing.Any], optional): 额外的参数. Defaults to {}.
 