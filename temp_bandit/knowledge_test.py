@@ -5,6 +5,7 @@
 from unittest.mock import patch
 
 import pytest
+from pydantic import ValidationError
 
 from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
 from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
@@ -37,26 +38,40 @@ def reset_knowledge_storage(mock_vector_db):
     yield
 
 
-def test_string_knowledge_source(mock_vector_db):
-    """"""Test StringKnowledgeSource with simple text content.""""""
-    content = ""Users name is John. He is 30 years old and lives in San Francisco.""
-    string_source = StringKnowledgeSource(content=content)
-    mock_vector_db.sources = [string_source]
-    mock_vector_db.query.return_value = [{""context"": content, ""score"": 0.9}]
-
-    # Test initialization
-    assert string_source.content == content
-    
-    # Test adding content
-    string_source.add()
-    assert len(string_source.chunks) > 0
-    
-    # Test querying
-    query = ""Where does John live?""
-    results = mock_vector_db.query(query)
-    assert len(results) > 0
-    assert ""San Francisco"" in results[0][""context""]
-    mock_vector_db.query.assert_called_once()
+class TestStringKnowledgeSource:
+    def test_initialization(self, mock_vector_db):
+        """"""Test basic initialization of StringKnowledgeSource.""""""
+        content = ""Users name is John. He is 30 years old and lives in San Francisco.""
+        string_source = StringKnowledgeSource(content=content)
+        assert string_source.content == content
+        assert string_source.storage is not None
+
+    def test_add_and_query(self, mock_vector_db):
+        """"""Test adding content and querying.""""""
+        content = ""Users name is John. He is 30 years old and lives in San Francisco.""
+        string_source = StringKnowledgeSource(content=content)
+        string_source.storage = mock_vector_db
+
+        mock_vector_db.query.return_value = [{""context"": content, ""score"": 0.9}]
+
+        string_source.add()
+        assert len(string_source.chunks) > 0
+
+        query = ""Where does John live?""
+        results = mock_vector_db.query(query)
+        assert len(results) > 0
+        assert ""San Francisco"" in results[0][""context""]
+        mock_vector_db.query.assert_called_once()
+
+    def test_empty_content(self, mock_vector_db):
+        """"""Test that empty content raises ValueError.""""""
+        with pytest.raises(ValueError, match=""StringKnowledgeSource only accepts string content""):
+            StringKnowledgeSource(content="""")
+
+    def test_non_string_content(self, mock_vector_db):
+        """"""Test that non-string content raises ValidationError.""""""
+        with pytest.raises(ValidationError, match=""Input should be a valid string""):
+            StringKnowledgeSource(content=123)
 
 
 def test_single_short_string(mock_vector_db):