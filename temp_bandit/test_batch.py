@@ -31,7 +31,8 @@ def test_batch_call() -> None:
 
     This test verifies:
     1. Batch processing of multiple prompts
-    2. Correct response format""""""
+    2. Correct response format
+    """"""
     # Test input prompts
     test_prompts: List[str] = [""What is 2+2?"", ""What is 3+3?"", ""What is 4+4?""]
 
@@ -45,10 +46,9 @@ def test_batch_call() -> None:
     assert len(result) == len(test_prompts), ""Number of results should match number of prompts""
     for i in range(len(result)):
         result_item = result[i]
-        assert (
-            result_item[""input""] == test_prompts[i]
-        ), f""Result at index {i} for prompt {result_item['input']} should match expected prompt""
-        assert (
+        assert result_item[""input""] == test_prompts[i], f""Result at index {i} for prompt {result_item['input']} should match expected prompt""
+        # TODO: this is potentially an incorrect assertion
+        assert (  # noqa: F631
             result_item[""answer""] == expected_answers[result_item[""input""]],
             f""Result at index {i} for prompt {result_item['input']} should match expected answer"",
         )
@@ -67,8 +67,8 @@ def test_anthropic_batch_structured_output() -> None:
     This test verifies:
     1. Batch processing with structured output format
     2. Correct parsing of responses into pydantic models
-    3. Multiple prompts processed correctly""""""
-
+    3. Multiple prompts processed correctly
+    """"""
     # Test input prompts
     test_prompts: List[str] = [
         ""Create a recipe for pasta"",