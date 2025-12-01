@@ -298,6 +298,7 @@ def _use(
 
         if original_tool and hasattr(original_tool, ""result_as_answer"") and original_tool.result_as_answer:
             result_as_answer = original_tool.result_as_answer
+            data[""result_as_answer""] = result_as_answer
         elif available_tool and hasattr(available_tool, ""result_as_answer"") and available_tool.result_as_answer:
             result_as_answer = available_tool.result_as_answer  # type: ignore # Item ""None"" of ""Any | None"" has no attribute ""result_as_answer""
             data[""result_as_answer""] = result_as_answer  # type: ignore