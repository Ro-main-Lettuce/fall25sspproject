@@ -12,7 +12,6 @@ def test_rag_storage_import_error(self):
         with patch.dict(sys.modules, {""chromadb"": None}):
             with pytest.raises(ImportError) as excinfo:
                 from crewai.memory.storage.rag_storage import RAGStorage
-                storage = RAGStorage(type=""test"")
             
             assert ""ChromaDB is not installed"" in str(excinfo.value)
 
@@ -21,6 +20,5 @@ def test_knowledge_storage_import_error(self):
         with patch.dict(sys.modules, {""chromadb"": None}):
             with pytest.raises(ImportError) as excinfo:
                 from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage
-                storage = KnowledgeStorage()
             
             assert ""ChromaDB is not installed"" in str(excinfo.value)