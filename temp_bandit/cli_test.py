@@ -27,7 +27,7 @@ def runner():
 
 
 @mock.patch(""crewai.cli.cli.train_crew"")
-def test_train_default_iterations(train_crew, runner):
+def test_train_default_iterations(train_crew, runner) -> None:
     result = runner.invoke(train)
 
     train_crew.assert_called_once_with(5, ""trained_agents_data.pkl"")
@@ -36,7 +36,7 @@ def test_train_default_iterations(train_crew, runner):
 
 
 @mock.patch(""crewai.cli.cli.train_crew"")
-def test_train_custom_iterations(train_crew, runner):
+def test_train_custom_iterations(train_crew, runner) -> None:
     result = runner.invoke(train, [""--n_iterations"", ""10""])
 
     train_crew.assert_called_once_with(10, ""trained_agents_data.pkl"")
@@ -45,7 +45,7 @@ def test_train_custom_iterations(train_crew, runner):
 
 
 @mock.patch(""crewai.cli.cli.train_crew"")
-def test_train_invalid_string_iterations(train_crew, runner):
+def test_train_invalid_string_iterations(train_crew, runner) -> None:
     result = runner.invoke(train, [""--n_iterations"", ""invalid""])
 
     train_crew.assert_not_called()
@@ -66,12 +66,12 @@ def mock_crew():
 @pytest.fixture
 def mock_get_crews(mock_crew):
     with mock.patch(
-        ""crewai.cli.reset_memories_command.get_crews"", return_value=[mock_crew]
+        ""crewai.cli.reset_memories_command.get_crews"", return_value=[mock_crew],
     ) as mock_get_crew:
         yield mock_get_crew
 
 
-def test_reset_all_memories(mock_get_crews, runner):
+def test_reset_all_memories(mock_get_crews, runner) -> None:
     result = runner.invoke(reset_memories, [""-a""])
 
     call_count = 0
@@ -86,7 +86,7 @@ def test_reset_all_memories(mock_get_crews, runner):
     assert call_count == 1, ""reset_memories should have been called once""
 
 
-def test_reset_short_term_memories(mock_get_crews, runner):
+def test_reset_short_term_memories(mock_get_crews, runner) -> None:
     result = runner.invoke(reset_memories, [""-s""])
     call_count = 0
     for crew in mock_get_crews.return_value:
@@ -99,7 +99,7 @@ def test_reset_short_term_memories(mock_get_crews, runner):
     assert call_count == 1, ""reset_memories should have been called once""
 
 
-def test_reset_entity_memories(mock_get_crews, runner):
+def test_reset_entity_memories(mock_get_crews, runner) -> None:
     result = runner.invoke(reset_memories, [""-e""])
     call_count = 0
     for crew in mock_get_crews.return_value:
@@ -110,7 +110,7 @@ def test_reset_entity_memories(mock_get_crews, runner):
     assert call_count == 1, ""reset_memories should have been called once""
 
 
-def test_reset_long_term_memories(mock_get_crews, runner):
+def test_reset_long_term_memories(mock_get_crews, runner) -> None:
     result = runner.invoke(reset_memories, [""-l""])
     call_count = 0
     for crew in mock_get_crews.return_value:
@@ -121,7 +121,7 @@ def test_reset_long_term_memories(mock_get_crews, runner):
     assert call_count == 1, ""reset_memories should have been called once""
 
 
-def test_reset_kickoff_outputs(mock_get_crews, runner):
+def test_reset_kickoff_outputs(mock_get_crews, runner) -> None:
     result = runner.invoke(reset_memories, [""-k""])
     call_count = 0
     for crew in mock_get_crews.return_value:
@@ -135,12 +135,12 @@ def test_reset_kickoff_outputs(mock_get_crews, runner):
     assert call_count == 1, ""reset_memories should have been called once""
 
 
-def test_reset_multiple_memory_flags(mock_get_crews, runner):
+def test_reset_multiple_memory_flags(mock_get_crews, runner) -> None:
     result = runner.invoke(reset_memories, [""-s"", ""-l""])
     call_count = 0
     for crew in mock_get_crews.return_value:
         crew.reset_memories.assert_has_calls(
-            [mock.call(command_type=""long""), mock.call(command_type=""short"")]
+            [mock.call(command_type=""long""), mock.call(command_type=""short"")],
         )
         assert (
             f""[Crew ({crew.name})] Long term memory has been reset.
""
@@ -151,7 +151,7 @@ def test_reset_multiple_memory_flags(mock_get_crews, runner):
     assert call_count == 1, ""reset_memories should have been called once""
 
 
-def test_reset_knowledge(mock_get_crews, runner):
+def test_reset_knowledge(mock_get_crews, runner) -> None:
     result = runner.invoke(reset_memories, [""--knowledge""])
     call_count = 0
     for crew in mock_get_crews.return_value:
@@ -162,7 +162,7 @@ def test_reset_knowledge(mock_get_crews, runner):
     assert call_count == 1, ""reset_memories should have been called once""
 
 
-def test_reset_memory_from_many_crews(mock_get_crews, runner):
+def test_reset_memory_from_many_crews(mock_get_crews, runner) -> None:
 
     crews = []
     for crew_id in [""id-1234"", ""id-5678""]:
@@ -185,7 +185,7 @@ def test_reset_memory_from_many_crews(mock_get_crews, runner):
     assert call_count == 2, ""reset_memories should have been called twice""
 
 
-def test_reset_no_memory_flags(runner):
+def test_reset_no_memory_flags(runner) -> None:
     result = runner.invoke(
         reset_memories,
     )
@@ -195,21 +195,21 @@ def test_reset_no_memory_flags(runner):
     )
 
 
-def test_version_flag(runner):
+def test_version_flag(runner) -> None:
     result = runner.invoke(version)
 
     assert result.exit_code == 0
     assert ""crewai version:"" in result.output
 
 
-def test_version_command(runner):
+def test_version_command(runner) -> None:
     result = runner.invoke(version)
 
     assert result.exit_code == 0
     assert ""crewai version:"" in result.output
 
 
-def test_version_command_with_tools(runner):
+def test_version_command_with_tools(runner) -> None:
     result = runner.invoke(version, [""--tools""])
 
     assert result.exit_code == 0
@@ -221,7 +221,7 @@ def test_version_command_with_tools(runner):
 
 
 @mock.patch(""crewai.cli.cli.evaluate_crew"")
-def test_test_default_iterations(evaluate_crew, runner):
+def test_test_default_iterations(evaluate_crew, runner) -> None:
     result = runner.invoke(test)
 
     evaluate_crew.assert_called_once_with(3, ""gpt-4o-mini"")
@@ -230,7 +230,7 @@ def test_test_default_iterations(evaluate_crew, runner):
 
 
 @mock.patch(""crewai.cli.cli.evaluate_crew"")
-def test_test_custom_iterations(evaluate_crew, runner):
+def test_test_custom_iterations(evaluate_crew, runner) -> None:
     result = runner.invoke(test, [""--n_iterations"", ""5"", ""--model"", ""gpt-4o""])
 
     evaluate_crew.assert_called_once_with(5, ""gpt-4o"")
@@ -239,7 +239,7 @@ def test_test_custom_iterations(evaluate_crew, runner):
 
 
 @mock.patch(""crewai.cli.cli.evaluate_crew"")
-def test_test_invalid_string_iterations(evaluate_crew, runner):
+def test_test_invalid_string_iterations(evaluate_crew, runner) -> None:
     result = runner.invoke(test, [""--n_iterations"", ""invalid""])
 
     evaluate_crew.assert_not_called()
@@ -251,7 +251,7 @@ def test_test_invalid_string_iterations(evaluate_crew, runner):
 
 
 @mock.patch(""crewai.cli.cli.AuthenticationCommand"")
-def test_signup(command, runner):
+def test_signup(command, runner) -> None:
     mock_auth = command.return_value
     result = runner.invoke(signup)
 
@@ -260,7 +260,7 @@ def test_signup(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_create(command, runner):
+def test_deploy_create(command, runner) -> None:
     mock_deploy = command.return_value
     result = runner.invoke(deploy_create)
 
@@ -269,7 +269,7 @@ def test_deploy_create(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_list(command, runner):
+def test_deploy_list(command, runner) -> None:
     mock_deploy = command.return_value
     result = runner.invoke(deploy_list)
 
@@ -278,7 +278,7 @@ def test_deploy_list(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_push(command, runner):
+def test_deploy_push(command, runner) -> None:
     mock_deploy = command.return_value
     uuid = ""test-uuid""
     result = runner.invoke(deploy_push, [""-u"", uuid])
@@ -288,7 +288,7 @@ def test_deploy_push(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_push_no_uuid(command, runner):
+def test_deploy_push_no_uuid(command, runner) -> None:
     mock_deploy = command.return_value
     result = runner.invoke(deploy_push)
 
@@ -297,7 +297,7 @@ def test_deploy_push_no_uuid(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_status(command, runner):
+def test_deploy_status(command, runner) -> None:
     mock_deploy = command.return_value
     uuid = ""test-uuid""
     result = runner.invoke(deply_status, [""-u"", uuid])
@@ -307,7 +307,7 @@ def test_deploy_status(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_status_no_uuid(command, runner):
+def test_deploy_status_no_uuid(command, runner) -> None:
     mock_deploy = command.return_value
     result = runner.invoke(deply_status)
 
@@ -316,7 +316,7 @@ def test_deploy_status_no_uuid(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_logs(command, runner):
+def test_deploy_logs(command, runner) -> None:
     mock_deploy = command.return_value
     uuid = ""test-uuid""
     result = runner.invoke(deploy_logs, [""-u"", uuid])
@@ -326,7 +326,7 @@ def test_deploy_logs(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_logs_no_uuid(command, runner):
+def test_deploy_logs_no_uuid(command, runner) -> None:
     mock_deploy = command.return_value
     result = runner.invoke(deploy_logs)
 
@@ -335,7 +335,7 @@ def test_deploy_logs_no_uuid(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_remove(command, runner):
+def test_deploy_remove(command, runner) -> None:
     mock_deploy = command.return_value
     uuid = ""test-uuid""
     result = runner.invoke(deploy_remove, [""-u"", uuid])
@@ -345,7 +345,7 @@ def test_deploy_remove(command, runner):
 
 
 @mock.patch(""crewai.cli.cli.DeployCommand"")
-def test_deploy_remove_no_uuid(command, runner):
+def test_deploy_remove_no_uuid(command, runner) -> None:
     mock_deploy = command.return_value
     result = runner.invoke(deploy_remove)
 
@@ -355,12 +355,11 @@ def test_deploy_remove_no_uuid(command, runner):
 
 @mock.patch(""crewai.cli.add_crew_to_flow.create_embedded_crew"")
 @mock.patch(""pathlib.Path.exists"", return_value=True)  # Mock the existence check
-def test_flow_add_crew(mock_path_exists, mock_create_embedded_crew, runner):
+def test_flow_add_crew(mock_path_exists, mock_create_embedded_crew, runner) -> None:
     crew_name = ""new_crew""
     result = runner.invoke(flow_add_crew, [crew_name])
 
     # Log the output for debugging
-    print(result.output)
 
     assert result.exit_code == 0, f""Command failed with output: {result.output}""
     assert f""Adding crew {crew_name} to the flow"" in result.output
@@ -373,11 +372,11 @@ def test_flow_add_crew(mock_path_exists, mock_create_embedded_crew, runner):
     assert isinstance(call_kwargs[""parent_folder""], Path)
 
 
-def test_add_crew_to_flow_not_in_root(runner):
+def test_add_crew_to_flow_not_in_root(runner) -> None:
     # Simulate not being in the root of a flow project
     with mock.patch(""pathlib.Path.exists"", autospec=True) as mock_exists:
         # Mock Path.exists to return False when checking for pyproject.toml
-        def exists_side_effect(self):
+        def exists_side_effect(self) -> bool:
             if self.name == ""pyproject.toml"":
                 return False  # Simulate that pyproject.toml does not exist
             return True  # All other paths exist
@@ -388,5 +387,5 @@ def exists_side_effect(self):
 
         assert result.exit_code != 0
         assert ""This command must be run from the root of a flow project."" in str(
-            result.output
+            result.output,
         )