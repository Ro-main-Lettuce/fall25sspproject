@@ -225,7 +225,7 @@ def override_api(self):
                         if api_key:
                             try:
                                 genai.configure(api_key=api_key)
-                                provider = GeminiProvider()
+                                provider = GeminiProvider(self.client)
                                 provider.override()
                             except Exception as e:
                                 logger.warning(f""Failed to initialize Gemini provider: {str(e)}"")