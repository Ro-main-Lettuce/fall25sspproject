@@ -1608,6 +1608,26 @@ def login(
     mock.assert_called_once()
 
 
+@pytest.mark.deepseek
+def test_conversable_agent_with_deepseek_reasoner(
+    credentials_deepseek_reasoner: Credentials,
+) -> None:
+    agent = ConversableAgent(
+        name=""agent"",
+        llm_config=credentials_deepseek_reasoner.llm_config,
+    )
+
+    user_proxy = UserProxyAgent(
+        name=""user_proxy_1"",
+        human_input_mode=""NEVER"",
+    )
+
+    result = user_proxy.initiate_chat(
+        agent, message=""Hello, how are you?"", summary_method=""reflection_with_llm"", max_turns=2
+    )
+    assert isinstance(result.summary, str)
+
+
 if __name__ == ""__main__"":
     # test_trigger()
     # test_context()