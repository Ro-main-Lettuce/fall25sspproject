@@ -7,32 +7,51 @@
 
 
 class TestCodeInterpreterTool(unittest.TestCase):
-    @patch(""crewai_tools.tools.code_interpreter_tool.code_interpreter_tool.docker"")
+    @patch(
+        ""crewai_tools.tools.code_interpreter_tool.code_interpreter_tool.docker_from_env""
+    )
     def test_run_code_in_docker(self, docker_mock):
         tool = CodeInterpreterTool()
         code = ""print('Hello, World!')""
         libraries_used = [""numpy"", ""pandas""]
         expected_output = ""Hello, World!
""
 
-        docker_mock.from_env().containers.run().exec_run().exit_code = 0
-        docker_mock.from_env().containers.run().exec_run().output = (
-            expected_output.encode()
-        )
+        docker_mock().containers.run().exec_run().exit_code = 0
+        docker_mock().containers.run().exec_run().output = expected_output.encode()
         result = tool.run_code_in_docker(code, libraries_used)
 
         self.assertEqual(result, expected_output)
 
-    @patch(""crewai_tools.tools.code_interpreter_tool.code_interpreter_tool.docker"")
+    @patch(
+        ""crewai_tools.tools.code_interpreter_tool.code_interpreter_tool.docker_from_env""
+    )
     def test_run_code_in_docker_with_error(self, docker_mock):
         tool = CodeInterpreterTool()
         code = ""print(1/0)""
         libraries_used = [""numpy"", ""pandas""]
         expected_output = ""Something went wrong while running the code: 
ZeroDivisionError: division by zero
""
 
-        docker_mock.from_env().containers.run().exec_run().exit_code = 1
-        docker_mock.from_env().containers.run().exec_run().output = (
+        docker_mock().containers.run().exec_run().exit_code = 1
+        docker_mock().containers.run().exec_run().output = (
             b""ZeroDivisionError: division by zero
""
         )
         result = tool.run_code_in_docker(code, libraries_used)
 
         self.assertEqual(result, expected_output)
+
+    @patch(
+        ""crewai_tools.tools.code_interpreter_tool.code_interpreter_tool.docker_from_env""
+    )
+    def test_run_code_in_docker_with_script(self, docker_mock):
+        tool = CodeInterpreterTool()
+        code = """"""print(""This is line 1"")
+print(""This is line 2"")""""""
+        libraries_used = []  # No additional libraries needed for this test
+        expected_output = ""This is line 1
This is line 2
""
+
+        # Mock Docker responses
+        docker_mock().containers.run().exec_run().exit_code = 0
+        docker_mock().containers.run().exec_run().output = expected_output.encode()
+
+        result = tool.run_code_in_docker(code, libraries_used)
+        self.assertEqual(result, expected_output)