@@ -38,13 +38,15 @@ def __init__(self, pipeline_configs: Dict[str, Dict], llm_client: OllamaClient,
         # 🚀 NEW: In-memory store for conversational history per session
         self.chat_histories: LRUCache = LRUCache(maxsize=100) # Stores history for 100 recent sessions
 
-        graph_config = self.pipeline_configs.get(""graph_strategy"", {})
+        graph_config = self.pipeline_configs.get(""retrieval"", {}).get(""graph"", {})
         if graph_config.get(""enabled""):
             self.graph_query_translator = GraphQueryTranslator(llm_client, gen_model)
-            self.graph_retriever = GraphRetriever(graph_config[""graph_path""])
-            print(""Agent initialized with live GraphRAG capabilities."")
+            from rag_system.retrieval.retrievers import NanoGraphRetriever
+            working_dir = graph_config.get(""working_dir"", ""./index_store/nano_graphrag"")
+            self.graph_retriever = NanoGraphRetriever(working_dir, llm_client, self.ollama_config)
+            print(""Agent initialized with nano-graphrag capabilities."")
         else:
-            print(""Agent initialized (GraphRAG disabled)."")
+            print(""Agent initialized (nano-graphrag disabled)."")
 
         # ---- Load document overviews for fast routing ----
         self._global_overview_path = os.path.join(""index_store"", ""overviews"", ""overviews.jsonl"")
@@ -220,14 +222,16 @@ async def _triage_query_async(self, query: str, history: list) -> str:
 
     def _run_graph_query(self, query: str, history: list) -> Dict[str, Any]:
         contextual_query = self._format_query_with_history(query, history)
-        structured_query = self.graph_query_translator.translate(contextual_query)
-        if not structured_query.get(""start_node""):
-            return self.retrieval_pipeline.run(contextual_query, window_size_override=0)
-        results = self.graph_retriever.retrieve(structured_query)
-        if not results:
-            return self.retrieval_pipeline.run(contextual_query, window_size_override=0)
-        answer = "", "".join([res['details']['node_id'] for res in results])
-        return {""answer"": f""From the knowledge graph: {answer}"", ""source_documents"": results}
+        
+        if hasattr(self.graph_retriever, 'retrieve'):
+            try:
+                results = self.graph_retriever.retrieve(contextual_query, mode=""local"")
+                if results:
+                    return {""answer"": results[0]['text'], ""source_documents"": results}
+            except Exception as e:
+                print(f""⚠️ nano-graphrag query failed: {e}"")
+        
+        return self.retrieval_pipeline.run(contextual_query, window_size_override=0)
 
     def _get_cache_key(self, query: str, query_type: str) -> str:
         """"""Generate a cache key for the query""""""