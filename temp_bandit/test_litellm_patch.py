@@ -2,11 +2,12 @@
 Test for the litellm patch that fixes the IndexError in ollama_pt function.
 """"""
 
-import unittest
-from unittest.mock import patch, MagicMock
 import sys
+import unittest
+from unittest.mock import MagicMock, patch
 
 import litellm
+import pytest
 from litellm.litellm_core_utils.prompt_templates.factory import ollama_pt
 
 from crewai.patches.litellm_patch import patch_litellm_ollama_pt
@@ -26,10 +27,11 @@ def test_ollama_pt_patch_fixes_index_error(self):
         
         try:
             # Apply the patch
-            patch_litellm_ollama_pt()
+            success = patch_litellm_ollama_pt()
+            self.assertTrue(success, ""Patch application failed"")
             
-            # The patched function should not raise an IndexError
-            result = ollama_pt(""qwen3:4b"", messages)
+            # Use the function from the module directly to ensure we're using the patched version
+            result = litellm.litellm_core_utils.prompt_templates.factory.ollama_pt(""qwen3:4b"", messages)
             
             # Verify the result is as expected
             self.assertIn(""prompt"", result)
@@ -39,6 +41,30 @@ def test_ollama_pt_patch_fixes_index_error(self):
         finally:
             # Restore the original function to avoid affecting other tests
             litellm.litellm_core_utils.prompt_templates.factory.ollama_pt = original_ollama_pt
+    
+    def test_ollama_pt_patch_with_empty_messages(self):
+        """"""Test that the patch handles empty message lists.""""""
+        messages = []
+        
+        # Store the original function to restore it after the test
+        original_ollama_pt = litellm.litellm_core_utils.prompt_templates.factory.ollama_pt
+        
+        try:
+            # Apply the patch
+            success = patch_litellm_ollama_pt()
+            self.assertTrue(success, ""Patch application failed"")
+            
+            # Use the function from the module directly to ensure we're using the patched version
+            result = litellm.litellm_core_utils.prompt_templates.factory.ollama_pt(""qwen3:4b"", messages)
+            
+            # Verify the result is as expected
+            self.assertIn(""prompt"", result)
+            self.assertIn(""images"", result)
+            self.assertEqual("""", result[""prompt""])
+            self.assertEqual([], result[""images""])
+        finally:
+            # Restore the original function to avoid affecting other tests
+            litellm.litellm_core_utils.prompt_templates.factory.ollama_pt = original_ollama_pt
 
 
 if __name__ == ""__main__"":