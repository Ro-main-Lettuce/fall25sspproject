@@ -28,7 +28,7 @@ class Document(Base):  # type: ignore
     
     id = Column(String, primary_key=True)
     content = Column(Text)
-    metadata = Column(Text)  # JSON serialized metadata
+    doc_metadata = Column(Text)  # JSON serialized metadata
     embedding: Column = Column(Vector(1536))  # Adjust dimension based on embedding model
 
 class PGVectorKnowledgeStorage(BaseKnowledgeStorage):
@@ -109,12 +109,16 @@ def search(
         try:
             query_embedding = self.embedder([query[0]])[0]
             
-            sql_query = text(f""""""
-            SELECT id, content, metadata, 1 - (embedding <=> :query_embedding) as similarity
-            FROM {self.table_name}
+            sql_query = text(""""""
+            SELECT id, content, doc_metadata, 1 - (embedding <=> :query_embedding) as similarity
+            FROM :table_name
             ORDER BY embedding <=> :query_embedding
             LIMIT :limit
-            """""")
+            """""").bindparams(
+                query_embedding=query_embedding,
+                limit=limit,
+                table_name=self.table_name
+            )
             
             results = session.execute(
                 sql_query, 
@@ -128,7 +132,7 @@ def search(
                     formatted_results.append({
                         ""id"": row[0],
                         ""context"": row[1],
-                        ""metadata"": row[2],
+                        ""metadata"": row[2],  # Keep the key as 'metadata' for API compatibility
                         ""score"": similarity,
                     })
             
@@ -173,13 +177,13 @@ def save(
                 
                 if existing:
                     setattr(existing, ""content"", doc)
-                    setattr(existing, ""metadata"", str(meta) if meta else None)
+                    setattr(existing, ""doc_metadata"", str(meta) if meta else None)
                     setattr(existing, ""embedding"", embedding)
                 else:
                     new_doc = Document(
                         id=doc_id,
                         content=doc,
-                        metadata=str(meta) if meta else None,
+                        doc_metadata=str(meta) if meta else None,
                         embedding=embedding,
                     )
                     session.add(new_doc)