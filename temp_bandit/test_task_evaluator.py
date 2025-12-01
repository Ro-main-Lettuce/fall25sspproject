@@ -8,7 +8,7 @@
 
 
 @patch(""crewai.utilities.evaluators.task_evaluator.Converter"")
-def test_evaluate_training_data(converter_mock):
+def test_evaluate_training_data(converter_mock) -> None:
     training_data = {
         ""agent_id"": {
             ""data1"": {
@@ -21,7 +21,7 @@ def test_evaluate_training_data(converter_mock):
                 ""human_feedback"": ""Human feedback 2"",
                 ""improved_output"": ""Improved output 2"",
             },
-        }
+        },
     }
     agent_id = ""agent_id""
     original_agent = MagicMock()
@@ -30,7 +30,7 @@ def test_evaluate_training_data(converter_mock):
         suggestions=[
             ""The initial output was already good, having a detailed explanation. However, the improved output ""
             ""gave similar information but in a more professional manner using better vocabulary. For future tasks, ""
-            ""try to implement more elaborate language and precise terminology from the beginning.""
+            ""try to implement more elaborate language and precise terminology from the beginning."",
         ],
         quality=8.0,
         final_summary=""The agent responded well initially. However, the improved output showed that there is room ""
@@ -39,7 +39,7 @@ def test_evaluate_training_data(converter_mock):
     )
     converter_mock.return_value.to_pydantic.return_value = function_return_value
     result = TaskEvaluator(original_agent=original_agent).evaluate_training_data(
-        training_data, agent_id
+        training_data, agent_id,
     )
 
     assert result == function_return_value
@@ -61,5 +61,5 @@ def test_evaluate_training_data(converter_mock):
                 ""following structure, with the following keys:
{
    suggestions: List[str],
    quality: float,
    final_summary: str
}"",
             ),
             mock.call().to_pydantic(),
-        ]
+        ],
     )