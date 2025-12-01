@@ -85,3 +85,46 @@ def test_memory_prioritizes_recent_topic(short_term_memory):
             
             # Verify that the scores reflect the recency prioritization
             assert results[0][""score""] > results[1][""score""], ""Recent topic should have higher score""
+
+
+def test_future_timestamp_validation():
+    """"""Test that ShortTermMemoryItem raises ValueError for future timestamps.""""""
+    # Setup agent and task for memory
+    agent = Agent(
+        role=""Tutor"",
+        goal=""Teach programming concepts"",
+        backstory=""You are a programming tutor helping students learn."",
+        tools=[],
+        verbose=True,
+    )
+    
+    task = Task(
+        description=""Explain programming concepts to students."",
+        expected_output=""Clear explanations of programming concepts."",
+        agent=agent,
+    )
+    
+    # Create a future timestamp
+    future_timestamp = datetime.now() + timedelta(days=1)
+    
+    # Test constructor validation
+    with pytest.raises(ValueError, match=""Timestamp cannot be in the future""):
+        ShortTermMemoryItem(data=""Test data"", timestamp=future_timestamp)
+    
+    # Test save method validation
+    memory = ShortTermMemory(crew=Crew(agents=[agent], tasks=[task]))
+    
+    # Create a memory item with a future timestamp
+    future_data = ""Test data with future timestamp""
+    
+    # We need to pass the data directly to the save method
+    # The save method will create a ShortTermMemoryItem internally
+    # and then we'll modify its timestamp before it's saved
+    
+    # Mock datetime.now to return a fixed time
+    with patch('crewai.memory.short_term.short_term_memory_item.datetime') as mock_datetime:
+        # Set up the mock to return our future timestamp when now() is called
+        mock_datetime.now.return_value = future_timestamp
+        
+        with pytest.raises(ValueError, match=""Cannot save memory item with future timestamp""):
+            memory.save(value=future_data)