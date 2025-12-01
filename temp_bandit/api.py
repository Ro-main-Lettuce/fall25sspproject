@@ -19,9 +19,9 @@
 from fastapi.middleware.cors import CORSMiddleware
 
 from llm_gateway.constants import AppEnv, get_settings
+from llm_gateway.routers.awsbedrock_api import router as AWSBedrockRouter
 from llm_gateway.routers.cohere_api import router as CohereRouter
 from llm_gateway.routers.openai_api import router as OpenAIRouter
-from llm_gateway.routers.awsbedrock_api import router as AWSBedrockRouter
 
 settings = get_settings()
 