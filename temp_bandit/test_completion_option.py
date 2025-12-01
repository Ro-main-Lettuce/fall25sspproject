@@ -51,7 +51,7 @@ def test_post_init_strips_trailing_quotes(self) -> None:
             type=""string"",
             completion_info=None,
         )
-        assert option3.name == 'test_string'
+        assert option3.name == ""test_string""
 
         # Test with no quotes
         option4 = CompletionOption(