@@ -155,11 +155,11 @@ def test_allowed_agents_validation():
     )
     assert agent.allowed_agents is None
     
-    with pytest.raises(ValueError, match=""Input should be a valid list""):
+    with pytest.raises(ValueError, match=""allowed_agents must be a list or tuple of agent roles""):
         Agent(
             role=""Test"",
             goal=""Test"",
-            backstory=""Test"", 
+            backstory=""Test"",
             allowed_agents=""invalid""
         )
     