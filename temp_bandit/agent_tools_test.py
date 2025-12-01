@@ -24,7 +24,7 @@ def vcr_config(request) -> dict:
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_delegate_work():
+def test_delegate_work() -> None:
     result = delegate_tool.run(
         coworker=""researcher"",
         task=""share your take on AI Agents"",
@@ -38,7 +38,7 @@ def test_delegate_work():
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_delegate_work_with_wrong_co_worker_variable():
+def test_delegate_work_with_wrong_co_worker_variable() -> None:
     result = delegate_tool.run(
         coworker=""researcher"",
         task=""share your take on AI Agents"",
@@ -52,7 +52,7 @@ def test_delegate_work_with_wrong_co_worker_variable():
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_ask_question():
+def test_ask_question() -> None:
     result = ask_tool.run(
         coworker=""researcher"",
         question=""do you hate AI Agents?"",
@@ -66,7 +66,7 @@ def test_ask_question():
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_ask_question_with_wrong_co_worker_variable():
+def test_ask_question_with_wrong_co_worker_variable() -> None:
     result = ask_tool.run(
         coworker=""researcher"",
         question=""do you hate AI Agents?"",
@@ -80,7 +80,7 @@ def test_ask_question_with_wrong_co_worker_variable():
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_delegate_work_withwith_coworker_as_array():
+def test_delegate_work_withwith_coworker_as_array() -> None:
     result = delegate_tool.run(
         coworker=""[researcher]"",
         task=""share your take on AI Agents"",
@@ -94,7 +94,7 @@ def test_delegate_work_withwith_coworker_as_array():
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_ask_question_with_coworker_as_array():
+def test_ask_question_with_coworker_as_array() -> None:
     result = ask_tool.run(
         coworker=""[researcher]"",
         question=""do you hate AI Agents?"",
@@ -107,7 +107,7 @@ def test_ask_question_with_coworker_as_array():
     )
 
 
-def test_delegate_work_to_wrong_agent():
+def test_delegate_work_to_wrong_agent() -> None:
     result = ask_tool.run(
         coworker=""writer"",
         question=""share your take on AI Agents"",
@@ -120,7 +120,7 @@ def test_delegate_work_to_wrong_agent():
     )
 
 
-def test_ask_question_to_wrong_agent():
+def test_ask_question_to_wrong_agent() -> None:
     result = ask_tool.run(
         coworker=""writer"",
         question=""do you hate AI Agents?"",