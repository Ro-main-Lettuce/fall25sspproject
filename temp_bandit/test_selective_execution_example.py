@@ -1,6 +1,5 @@
 """"""Example demonstrating selective execution for issue #2941.""""""
 
-import pytest
 from crewai import Agent, Crew, Task, Process
 
 
@@ -35,11 +34,11 @@ def test_issue_2941_example():
     }
     
     selector = crew.task_selector
-    assert selector(inputs, forecast_task) == True
-    assert selector(inputs, holiday_task) == False
-    assert selector(inputs, macro_task) == False
-    assert selector(inputs, news_task) == False
-    assert selector(inputs, query_task) == False
+    assert selector(inputs, forecast_task) is True
+    assert selector(inputs, holiday_task) is False
+    assert selector(inputs, macro_task) is False
+    assert selector(inputs, news_task) is False
+    assert selector(inputs, query_task) is False
 
 
 def test_multiple_actions_example():
@@ -61,14 +60,14 @@ def test_multiple_actions_example():
     
     selector = crew.task_selector
     
-    assert selector({""action"": ""research""}, research_task) == True
-    assert selector({""action"": ""research""}, analysis_task) == False
-    assert selector({""action"": ""research""}, writing_task) == False
+    assert selector({""action"": ""research""}, research_task) is True
+    assert selector({""action"": ""research""}, analysis_task) is False
+    assert selector({""action"": ""research""}, writing_task) is False
     
-    assert selector({""action"": ""analysis""}, research_task) == False
-    assert selector({""action"": ""analysis""}, analysis_task) == True
-    assert selector({""action"": ""analysis""}, writing_task) == False
+    assert selector({""action"": ""analysis""}, research_task) is False
+    assert selector({""action"": ""analysis""}, analysis_task) is True
+    assert selector({""action"": ""analysis""}, writing_task) is False
     
-    assert selector({""action"": ""writing""}, research_task) == False
-    assert selector({""action"": ""writing""}, analysis_task) == False
-    assert selector({""action"": ""writing""}, writing_task) == True
+    assert selector({""action"": ""writing""}, research_task) is False
+    assert selector({""action"": ""writing""}, analysis_task) is False
+    assert selector({""action"": ""writing""}, writing_task) is True