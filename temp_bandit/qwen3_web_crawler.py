@@ -16,12 +16,11 @@ class Colors:
 load_dotenv()
 
 firecrawl_api_key = os.getenv(""FIRECRAWL_API_KEY"")
-openai_api_key = os.getenv(""OPENAI_API_KEY"")
 openrouter_api_key = os.getenv(""OPENROUTER_API_KEY"")
 
 app = FirecrawlApp(api_key=firecrawl_api_key)
 client = OpenAI(
-    api_key=openai_api_key or openrouter_api_key,
+    api_key=openrouter_api_key,
     base_url=""https://openrouter.ai/api/v1""
 )
 