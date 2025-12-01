@@ -4119,20 +4119,53 @@ def test_crew_kickoff_for_each_works_with_manager_agent_copy():
     assert crew_copy.manager_agent.role == crew.manager_agent.role
     assert crew_copy.manager_agent.goal == crew.manager_agent.goal
 
-def test_crew_train_with_memory():
-    """"""Test that training a crew with memory enabled does not raise validation errors.""""""
+def test_crew_copy_with_memory():
+    """"""Test that copying a crew with memory enabled does not raise validation errors and copies memory correctly.""""""
     agent = Agent(role=""Test Agent"", goal=""Test Goal"", backstory=""Test Backstory"")
     task = Task(description=""Test Task"", expected_output=""Test Output"", agent=agent)
     crew = Crew(agents=[agent], tasks=[task], memory=True)
 
-    with tempfile.TemporaryDirectory() as tmpdir:
-        filename = os.path.join(tmpdir, ""training_data.pkl"")
-        try:
-            crew.train(n_iterations=1, filename=filename)
-        except pydantic_core.ValidationError as e:
-             if ""Input should be an instance of"" in str(e) and (""Memory"" in str(e)):
-                  pytest.fail(f""Training with memory raised Pydantic ValidationError, likely due to incorrect memory copy: {e}"")
-             else:
-                  raise e
-        except Exception as e:
-            print(f""Warning: Training raised an unexpected exception: {e}"")
+    original_short_term_id = id(crew._short_term_memory) if crew._short_term_memory else None
+    original_long_term_id = id(crew._long_term_memory) if crew._long_term_memory else None
+    original_entity_id = id(crew._entity_memory) if crew._entity_memory else None
+    original_external_id = id(crew._external_memory) if crew._external_memory else None
+    original_user_id = id(crew._user_memory) if crew._user_memory else None
+
+
+    try:
+        crew_copy = crew.copy()
+
+        assert hasattr(crew_copy, ""_short_term_memory""), ""Copied crew should have _short_term_memory""
+        assert crew_copy._short_term_memory is not None, ""Copied _short_term_memory should not be None""
+        assert id(crew_copy._short_term_memory) != original_short_term_id, ""Copied _short_term_memory should be a new object""
+
+        assert hasattr(crew_copy, ""_long_term_memory""), ""Copied crew should have _long_term_memory""
+        assert crew_copy._long_term_memory is not None, ""Copied _long_term_memory should not be None""
+        assert id(crew_copy._long_term_memory) != original_long_term_id, ""Copied _long_term_memory should be a new object""
+
+        assert hasattr(crew_copy, ""_entity_memory""), ""Copied crew should have _entity_memory""
+        assert crew_copy._entity_memory is not None, ""Copied _entity_memory should not be None""
+        assert id(crew_copy._entity_memory) != original_entity_id, ""Copied _entity_memory should be a new object""
+
+        if original_external_id:
+             assert hasattr(crew_copy, ""_external_memory""), ""Copied crew should have _external_memory""
+             assert crew_copy._external_memory is not None, ""Copied _external_memory should not be None""
+             assert id(crew_copy._external_memory) != original_external_id, ""Copied _external_memory should be a new object""
+        else:
+             assert not hasattr(crew_copy, ""_external_memory"") or crew_copy._external_memory is None, ""Copied _external_memory should be None if not originally present""
+
+        if original_user_id:
+             assert hasattr(crew_copy, ""_user_memory""), ""Copied crew should have _user_memory""
+             assert crew_copy._user_memory is not None, ""Copied _user_memory should not be None""
+             assert id(crew_copy._user_memory) != original_user_id, ""Copied _user_memory should be a new object""
+        else:
+             assert not hasattr(crew_copy, ""_user_memory"") or crew_copy._user_memory is None, ""Copied _user_memory should be None if not originally present""
+
+
+    except pydantic_core.ValidationError as e:
+         if ""Input should be an instance of"" in str(e) and (""Memory"" in str(e)):
+              pytest.fail(f""Copying with memory raised Pydantic ValidationError, likely due to incorrect memory copy: {e}"")
+         else:
+              raise e # Re-raise other validation errors
+    except Exception as e:
+        pytest.fail(f""Copying crew raised an unexpected exception: {e}"")