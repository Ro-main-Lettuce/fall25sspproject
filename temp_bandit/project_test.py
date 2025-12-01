@@ -184,3 +184,68 @@ def crew(self):
     assert ""plants"" in result.raw, ""First before_kickoff not executed""
     assert ""processed first"" in result.raw, ""First after_kickoff not executed""
     assert ""processed second"" in result.raw, ""Second after_kickoff not executed""
+
+
+@pytest.mark.vcr(filter_headers=[""authorization""])
+def test_multiple_yaml_configs():
+    @CrewBase
+    class MultiConfigCrew:
+        agents_config = [""config/multi/agents1.yaml"", ""config/multi/agents2.yaml""]
+        tasks_config = [""config/multi/tasks1.yaml"", ""config/multi/tasks2.yaml""]
+
+        @agent
+        def test_agent1(self):
+            return Agent(config=self.agents_config[""test_agent1""])
+
+        @agent
+        def test_agent2(self):
+            return Agent(config=self.agents_config[""test_agent2""])
+
+        @task
+        def test_task1(self):
+            task_config = self.tasks_config[""test_task1""].copy()
+            if isinstance(task_config.get(""agent""), str):
+                agent_name = task_config.pop(""agent"")
+                if hasattr(self, agent_name):
+                    task_config[""agent""] = getattr(self, agent_name)()
+            return Task(config=task_config)
+
+        @task
+        def test_task2(self):
+            task_config = self.tasks_config[""test_task2""].copy()
+            if isinstance(task_config.get(""agent""), str):
+                agent_name = task_config.pop(""agent"")
+                if hasattr(self, agent_name):
+                    task_config[""agent""] = getattr(self, agent_name)()
+            return Task(config=task_config)
+
+        @crew
+        def crew(self):
+            return Crew(agents=self.agents, tasks=self.tasks, verbose=True)
+
+    crew = MultiConfigCrew()
+    
+    assert ""test_agent1"" in crew.agents_config
+    assert ""test_agent2"" in crew.agents_config
+    
+    assert crew.agents_config[""test_agent1""][""role""] == ""Updated Test Agent 1""
+    assert crew.agents_config[""test_agent1""][""goal""] == ""Updated Test Goal 1""
+    assert crew.agents_config[""test_agent1""][""backstory""] == ""Test Backstory 1""
+    assert crew.agents_config[""test_agent1""][""verbose""] is True
+    
+    assert ""test_task1"" in crew.tasks_config
+    assert ""test_task2"" in crew.tasks_config
+    
+    assert crew.tasks_config[""test_task1""][""description""] == ""Updated Test Description 1""
+    assert crew.tasks_config[""test_task1""][""expected_output""] == ""Test Output 1""
+    assert crew.tasks_config[""test_task1""][""agent""].role == ""Updated Test Agent 1""
+
+    agent1 = crew.test_agent1()
+    agent2 = crew.test_agent2()
+    task1 = crew.test_task1()
+    task2 = crew.test_task2()
+    
+    assert agent1.role == ""Updated Test Agent 1""
+    assert agent2.role == ""Test Agent 2""
+    assert task1.description == ""Updated Test Description 1""
+    assert task2.description == ""Test Description 2""