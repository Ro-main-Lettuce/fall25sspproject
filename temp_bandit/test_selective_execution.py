@@ -1,4 +1,3 @@
-import pytest
 from crewai import Agent, Crew, Task, Process
 
 def test_selective_execution_basic():
@@ -41,12 +40,12 @@ def test_selective_execution_basic():
     selector = crew.task_selector
     
     inputs = {""action"": ""forecast""}
-    assert selector(inputs, forecast_task) == True
-    assert selector(inputs, news_task) == False
+    assert selector(inputs, forecast_task) is True
+    assert selector(inputs, news_task) is False
     
     inputs = {""action"": ""news""}
-    assert selector(inputs, forecast_task) == False
-    assert selector(inputs, news_task) == True
+    assert selector(inputs, forecast_task) is False
+    assert selector(inputs, news_task) is True
     
     print(""All selective execution tests passed!"")
 
@@ -67,7 +66,7 @@ def test_selective_process_validation():
     )
     
     try:
-        crew = Crew(
+        Crew(
             agents=[researcher],
             tasks=[task],
             process=Process.selective
@@ -101,10 +100,10 @@ def test_tag_selector_edge_cases():
     
     selector = Crew.create_tag_selector()
     
-    assert selector({}, tagged_task) == True
-    assert selector({}, untagged_task) == True
+    assert selector({}, tagged_task) is True
+    assert selector({}, untagged_task) is True
     
-    assert selector({""action"": ""anything""}, untagged_task) == True
+    assert selector({""action"": ""anything""}, untagged_task) is True
     
     print(""Edge case tests passed!"")
 