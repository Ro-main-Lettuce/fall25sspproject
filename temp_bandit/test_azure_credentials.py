@@ -1,6 +1,8 @@
 import pytest
+
 from src.crewai.llm import LLM
 
+
 def test_azure_detection_with_credentials():
     """"""Test that Azure is detected correctly when credentials are provided but model lacks azure/ prefix.""""""
     # Create LLM instance with Azure parameters but without azure/ prefix