@@ -8,13 +8,15 @@
 
 def test_import_without_chromadb():
     """"""Test that crewai can be imported without chromadb.""""""
-    with patch.dict(sys.modules, {""chromadb"": None}):
-        if ""crewai.memory.storage.rag_storage"" in sys.modules:
-            importlib.reload(sys.modules[""crewai.memory.storage.rag_storage""])
-        if ""crewai.knowledge.storage.knowledge_storage"" in sys.modules:
-            importlib.reload(sys.modules[""crewai.knowledge.storage.knowledge_storage""])
-        if ""crewai.utilities.embedding_configurator"" in sys.modules:
-            importlib.reload(sys.modules[""crewai.utilities.embedding_configurator""])
+    with patch.dict(sys.modules, {""chromadb"": None, ""chromadb.errors"": None, ""chromadb.api"": None, ""chromadb.config"": None}):
+        modules_to_reload = [
+            ""crewai.memory.storage.rag_storage"",
+            ""crewai.knowledge.storage.knowledge_storage"", 
+            ""crewai.utilities.embedding_configurator""
+        ]
+        for module in modules_to_reload:
+            if module in sys.modules:
+                importlib.reload(sys.modules[module])
             
         from crewai import Agent, Task, Crew, Process
         
@@ -25,7 +27,7 @@ def test_import_without_chromadb():
 
 def test_memory_storage_without_chromadb():
     """"""Test that memory storage raises appropriate error when chromadb is not available.""""""
-    with patch.dict(sys.modules, {""chromadb"": None}):
+    with patch.dict(sys.modules, {""chromadb"": None, ""chromadb.errors"": None, ""chromadb.api"": None, ""chromadb.config"": None}):
         if ""crewai.memory.storage.rag_storage"" in sys.modules:
             importlib.reload(sys.modules[""crewai.memory.storage.rag_storage""])
             
@@ -34,17 +36,21 @@ def test_memory_storage_without_chromadb():
         assert not HAS_CHROMADB
         
         with pytest.raises(ChromaDBRequiredError) as excinfo:
-            storage = RAGStorage()
-            storage._initialize_app()
+            storage = RAGStorage(""memory"", allow_reset=True, crew=None)
             
-        assert ""ChromaDB is required for memory storage features"" in str(excinfo.value)
+        assert ""ChromaDB is required for memory storage"" in str(excinfo.value)
 
 
 def test_knowledge_storage_without_chromadb():
     """"""Test that knowledge storage raises appropriate error when chromadb is not available.""""""
-    with patch.dict(sys.modules, {""chromadb"": None}):
-        if ""crewai.knowledge.storage.knowledge_storage"" in sys.modules:
-            importlib.reload(sys.modules[""crewai.knowledge.storage.knowledge_storage""])
+    with patch.dict(sys.modules, {""chromadb"": None, ""chromadb.errors"": None, ""chromadb.api"": None, ""chromadb.config"": None}):
+        modules_to_reload = [
+            ""crewai.knowledge.storage.knowledge_storage"",
+            ""crewai.utilities.embedding_configurator""
+        ]
+        for module in modules_to_reload:
+            if module in sys.modules:
+                importlib.reload(sys.modules[module])
             
         from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage, HAS_CHROMADB
         
@@ -54,12 +60,12 @@ def test_knowledge_storage_without_chromadb():
             storage = KnowledgeStorage()
             storage.initialize_knowledge_storage()
             
-        assert ""ChromaDB is required for knowledge storage features"" in str(excinfo.value)
+        assert ""ChromaDB is required for knowledge storage"" in str(excinfo.value)
 
 
 def test_embedding_configurator_without_chromadb():
     """"""Test that embedding configurator raises appropriate error when chromadb is not available.""""""
-    with patch.dict(sys.modules, {""chromadb"": None}):
+    with patch.dict(sys.modules, {""chromadb"": None, ""chromadb.errors"": None, ""chromadb.api"": None, ""chromadb.config"": None}):
         if ""crewai.utilities.embedding_configurator"" in sys.modules:
             importlib.reload(sys.modules[""crewai.utilities.embedding_configurator""])
             