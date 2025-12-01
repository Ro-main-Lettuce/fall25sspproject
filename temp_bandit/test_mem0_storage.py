@@ -29,7 +29,7 @@ def mem0_storage_with_mocked_config(mock_mem0_memory):
     """"""Fixture to create a Mem0Storage instance with mocked dependencies""""""
 
     # Patch the Memory class to return our mock
-    with patch(""mem0.memory.main.Memory.from_config"", return_value=mock_mem0_memory):
+    with patch(""mem0.memory.main.Memory.from_config"", return_value=mock_mem0_memory) as mock_from_config:
         config = {
             ""vector_store"": {
                 ""provider"": ""mock_vector_store"",
@@ -66,13 +66,15 @@ def mem0_storage_with_mocked_config(mock_mem0_memory):
         )
 
         mem0_storage = Mem0Storage(type=""short_term"", crew=crew)
-        return mem0_storage
+        return mem0_storage, mock_from_config, config
 
 
 def test_mem0_storage_initialization(mem0_storage_with_mocked_config, mock_mem0_memory):
     """"""Test that Mem0Storage initializes correctly with the mocked config""""""
-    assert mem0_storage_with_mocked_config.memory_type == ""short_term""
-    assert mem0_storage_with_mocked_config.memory is mock_mem0_memory
+    mem0_storage, mock_from_config, config = mem0_storage_with_mocked_config
+    assert mem0_storage.memory_type == ""short_term""
+    assert mem0_storage.memory is mock_mem0_memory
+    mock_from_config.assert_called_once_with(config)
 
 
 @pytest.fixture