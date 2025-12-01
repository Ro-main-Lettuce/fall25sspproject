@@ -26,7 +26,7 @@ def verify_documents(
 
     Args:
         state (DocVerificationInput): The current state
-        config (RunnableConfig): Configuration containing ProSearchConfig
+        config (RunnableConfig): Configuration containing AgentSearchConfig
 
     Updates:
         verified_documents: list[InferenceSection]