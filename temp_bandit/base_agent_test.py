@@ -7,7 +7,7 @@
 from crewai.tools.base_tool import BaseTool
 
 
-class TestAgent(BaseAgent):
+class MockAgent(BaseAgent):
     def execute_task(
         self,
         task: Any,
@@ -29,7 +29,7 @@ def get_output_converter(
 
 
 def test_key():
-    agent = TestAgent(
+    agent = MockAgent(
         role=""test role"",
         goal=""test goal"",
         backstory=""test backstory"",