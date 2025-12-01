@@ -170,7 +170,7 @@ def test_crew_external_memory_save_with_memory_flag(
     mem_method, crew_with_external_memory
 ):
     try:
-        import chromadb
+        import chromadb  # noqa: F401
         HAS_CHROMADB = True
     except ImportError:
         HAS_CHROMADB = False
@@ -190,6 +190,15 @@ def test_crew_external_memory_save_with_memory_flag(
 def test_crew_external_memory_save_using_crew_without_memory_flag(
     mem_method, crew_with_external_memory_without_memory_flag
 ):
+    try:
+        import chromadb  # noqa: F401
+        HAS_CHROMADB = True
+    except ImportError:
+        HAS_CHROMADB = False
+        
+    if not HAS_CHROMADB:
+        pytest.skip(""ChromaDB is required for this test"")
+        
     with patch(
         f""crewai.memory.external.external_memory.ExternalMemory.{mem_method}""
     ) as mock_method: