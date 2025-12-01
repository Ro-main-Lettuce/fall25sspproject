@@ -119,7 +119,13 @@ def _get_bm25_retriever(self):
 
     def _get_graph_retriever(self):
         if self._graph_retriever is None and self.retriever_configs.get(""graph"", {}).get(""enabled""):
-            self._graph_retriever = GraphRetriever(graph_path=self.storage_config[""graph_path""])
+            from rag_system.retrieval.retrievers import NanoGraphRetriever
+            working_dir = self.retriever_configs[""graph""].get(""working_dir"", ""./index_store/nano_graphrag"")
+            self._graph_retriever = NanoGraphRetriever(
+                working_dir=working_dir,
+                ollama_client=self.ollama_client,
+                ollama_config=self.ollama_config
+            )
         return self._graph_retriever
 
     def _get_reranker(self):
@@ -283,6 +289,23 @@ def run(self, query: str, table_name: str = None, window_size_override: Optional
                 reranker=lancedb_reranker # Pass the reranker to enable hybrid search
             )
 
+        # ---------------------------------------------------------------
+        # Graph retrieval (optional)
+        # ---------------------------------------------------------------
+        graph_retriever = self._get_graph_retriever()
+        if graph_retriever:
+            graph_mode = self.retriever_configs.get(""graph"", {}).get(""mode"", ""local"")
+            try:
+                graph_docs = graph_retriever.retrieve(query, mode=graph_mode, k=retrieval_k)
+                if graph_docs:
+                    fusion_weight = self.retriever_configs.get(""graph"", {}).get(""fusion_weight"", 0.4)
+                    for doc in graph_docs:
+                        doc['score'] = doc.get('score', 1.0) * fusion_weight
+                    retrieved_docs.extend(graph_docs)
+                    print(f""Added {len(graph_docs)} graph results to retrieval."")
+            except Exception as e:
+                print(f""⚠️ Graph retrieval failed: {e}"")
+
         # ---------------------------------------------------------------
         # Late-Chunk retrieval (optional)
         # ---------------------------------------------------------------
@@ -570,4 +593,4 @@ def update_embedding_model(self, model_name: str):
         self.config[""embedding_model_name""] = model_name
         # Reset caches so new instances are built on demand
         self.text_embedder = None
-        self.dense_retriever = None
\ No newline at end of file
+        self.dense_retriever = None