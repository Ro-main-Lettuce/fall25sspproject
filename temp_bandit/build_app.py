@@ -90,11 +90,11 @@ async def run(self, ap: app.Application):
         user_service_inst = user_service.UserService(ap)
         ap.user_service = user_service_inst
 
-        model_service_inst = model_service.ModelsService(ap)
-        ap.model_service = model_service_inst
-        
-        embeddings_models_service_inst = model_service.EmbeddingsModelsService(ap)
-        ap.embeddings_models_service = embeddings_models_service_inst
+        llm_model_service_inst = model_service.LLMModelsService(ap)
+        ap.llm_model_service = llm_model_service_inst
+
+        embedding_models_service_inst = model_service.EmbeddingModelsService(ap)
+        ap.embedding_models_service = embedding_models_service_inst
 
         pipeline_service_inst = pipeline_service.PipelineService(ap)
         ap.pipeline_service = pipeline_service_inst