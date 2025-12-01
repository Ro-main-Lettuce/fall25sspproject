@@ -40,7 +40,7 @@ def mock_vector_db():
 
 def test_agent_invalid_embedder_config():
     """"""Test that an invalid embedder configuration raises a ValueError.""""""
-    with pytest.raises(ValueError, match=""embedder_config must be a dictionary""):
+    with pytest.raises(ValueError, match=""Input should be a valid dictionary""):
         Agent(
             role=""test role"",
             goal=""test goal"",