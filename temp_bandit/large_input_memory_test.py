@@ -50,3 +50,37 @@ def test_memory_with_large_input(short_term_memory):
         result = short_term_memory.search(large_input[:100], score_threshold=0.01)
         assert result[0][""context""] == large_input
         assert result[0][""metadata""][""agent""] == ""test_agent""
+
+
+def test_memory_with_empty_input(short_term_memory):
+    """"""Test that memory correctly handles empty input strings""""""
+    empty_input = """"
+    
+    with patch.object(
+        short_term_memory.storage, '_chunk_text', 
+        return_value=[]
+    ) as mock_chunk_text:
+        with patch.object(
+            short_term_memory.storage.collection, 'add'
+        ) as mock_add:
+            short_term_memory.save(value=empty_input, agent=""test_agent"")
+            
+            mock_chunk_text.assert_called_with(empty_input)
+            mock_add.assert_not_called()
+
+
+def test_memory_with_exact_chunk_size_input(short_term_memory):
+    """"""Test that memory correctly handles inputs that match chunk size exactly""""""
+    exact_size_input = ""x"" * MEMORY_CHUNK_SIZE
+    
+    with patch.object(
+        short_term_memory.storage, '_chunk_text', 
+        return_value=[exact_size_input]
+    ) as mock_chunk_text:
+        with patch.object(
+            short_term_memory.storage.collection, 'add'
+        ) as mock_add:
+            short_term_memory.save(value=exact_size_input, agent=""test_agent"")
+            
+            mock_chunk_text.assert_called_with(exact_size_input)
+            assert mock_add.call_count == 1