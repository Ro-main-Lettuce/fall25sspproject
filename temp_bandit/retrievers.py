@@ -196,5 +196,49 @@ def _run_vec():
             return []
 # endregion
 
+
+class NanoGraphRetriever:
+    """"""Enhanced graph retriever using nano-graphrag.""""""
+    
+    def __init__(self, working_dir: str, ollama_client, ollama_config: Dict[str, Any]):
+        from rag_system.indexing.nano_graph_adapter import NanoGraphRAGAdapter
+        self.nano_graph_adapter = NanoGraphRAGAdapter(
+            working_dir=working_dir,
+            ollama_client=ollama_client,
+            ollama_config=ollama_config
+        )
+        self.default_mode = ""local""
+    
+    def retrieve(self, query: str, mode: str = None, k: int = 5) -> List[Dict[str, Any]]:
+        """"""Retrieve using nano-graphrag with specified mode.""""""
+        mode = mode or self.default_mode
+        
+        print(f""
--- Performing nano-graphrag Retrieval (mode: {mode}) for query: '{query}' ---"")
+        
+        try:
+            result = self.nano_graph_adapter.query(query, mode=mode)
+            
+            if result:
+                retrieved_docs = [{
+                    'chunk_id': f""nano_graph_{mode}_{hash(query)}"",
+                    'text': result,
+                    'score': 1.0,
+                    'metadata': {
+                        'source': 'nano_graphrag',
+                        'mode': mode,
+                        'query': query
+                    }
+                }]
+                print(f""Retrieved {len(retrieved_docs)} documents from nano-graphrag."")
+                return retrieved_docs[:k]
+            else:
+                print(""No results from nano-graphrag."")
+                return []
+                
+        except Exception as e:
+            print(f""⚠️ Error in nano-graphrag retrieval: {e}"")
+            return []
+
+
 if __name__ == '__main__':
     print(""retrievers.py updated for LanceDB FTS Hybrid Search."")