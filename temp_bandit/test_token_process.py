@@ -4,7 +4,10 @@
 
 
 class TestTokenProcess(unittest.TestCase):
+    """"""Test suite for TokenProcess class token counting functionality.""""""
+
     def setUp(self):
+        """"""Initialize a fresh TokenProcess instance before each test.""""""
         self.token_process = TokenProcess()
 
     def test_sum_cached_prompt_tokens_with_none(self):