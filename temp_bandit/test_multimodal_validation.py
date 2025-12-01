@@ -6,9 +6,8 @@
 
 
 @pytest.mark.skip(reason=""Only run manually with valid API keys"")
-def test_multimodal_agent_with_image_url():
-    """"""
-    Test that a multimodal agent can process images without validation errors.
+def test_multimodal_agent_with_image_url() -> None:
+    """"""Test that a multimodal agent can process images without validation errors.
     This test reproduces the scenario from issue #2475.
     """"""
     OPENAI_API_KEY = os.getenv(""OPENAI_API_KEY"")
@@ -18,7 +17,7 @@ def test_multimodal_agent_with_image_url():
     llm = LLM(
         model=""openai/gpt-4o"",  # model with vision capabilities
         api_key=OPENAI_API_KEY,
-        temperature=0.7
+        temperature=0.7,
     )
 
     expert_analyst = Agent(
@@ -28,7 +27,7 @@ def test_multimodal_agent_with_image_url():
         llm=llm,
         verbose=True,
         allow_delegation=False,
-        multimodal=True
+        multimodal=True,
     )
 
     inspection_task = Task(
@@ -40,7 +39,7 @@ def test_multimodal_agent_with_image_url():
         Provide a detailed report highlighting any issues found.
         """""",
         expected_output=""A detailed report highlighting any issues found"",
-        agent=expert_analyst
+        agent=expert_analyst,
     )
 
-    crew = Crew(agents=[expert_analyst], tasks=[inspection_task])
+    Crew(agents=[expert_analyst], tasks=[inspection_task])