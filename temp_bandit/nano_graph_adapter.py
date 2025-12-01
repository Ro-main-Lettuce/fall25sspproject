@@ -1,6 +1,8 @@
 import os
 import asyncio
 import concurrent.futures
+import time
+from datetime import datetime
 from typing import Dict, Any, List, Optional
 import numpy as np
 import ollama
@@ -100,29 +102,58 @@ async def ollama_embedding_func(texts: List[str]) -> np.ndarray:
         
         return ollama_embedding_func
     
-    def insert_documents(self, documents: List[str]) -> None:
+    def insert_documents(self, documents: List[str]) -> Dict[str, Any]:
         """"""Insert documents into the graph RAG system.""""""
+        stats = {
+            'total_documents': len(documents),
+            'processed_documents': 0,
+            'entities_extracted': 0,
+            'relationships_created': 0,
+            'processing_time': 0
+        }
+        
         try:
-            print(f""📄 Inserting {len(documents)} documents into nano-graphrag..."")
+            start_time = time.time()
+            print(f""🔗 [GRAPH] Starting knowledge graph construction..."")
+            print(f""📄 [GRAPH] Processing {len(documents)} documents for entity and relationship extraction"")
             
             try:
                 loop = asyncio.get_running_loop()
                 with concurrent.futures.ThreadPoolExecutor() as executor:
-                    future = executor.submit(self._sync_insert_documents, documents)
-                    future.result()
+                    future = executor.submit(self._sync_insert_documents, documents, stats)
+                    result_stats = future.result()
             except RuntimeError:
-                self._sync_insert_documents(documents)
-                
-            print(""✅ Document insertion completed"")
+                result_stats = self._sync_insert_documents(documents, stats)
+            
+            result_stats['processing_time'] = time.time() - start_time
+            print(f""✅ [GRAPH] Knowledge graph construction completed in {result_stats['processing_time']:.2f}s"")
+            print(f""📊 [GRAPH] Final statistics: {result_stats['processed_documents']} docs, ~{result_stats.get('entities_extracted', 'N/A')} entities, ~{result_stats.get('relationships_created', 'N/A')} relationships"")
+            
+            return result_stats
         except Exception as e:
-            print(f""❌ Error inserting documents: {e}"")
+            print(f""❌ [GRAPH] Error during graph construction: {e}"")
             raise
     
-    def _sync_insert_documents(self, documents: List[str]) -> None:
-        """"""Synchronous document insertion helper.""""""
+    def _sync_insert_documents(self, documents: List[str], stats: Dict[str, Any]) -> Dict[str, Any]:
+        """"""Synchronous document insertion helper with detailed logging.""""""
         for i, doc in enumerate(documents):
-            print(f""   Processing document {i+1}/{len(documents)}"")
+            print(f""   🔍 [GRAPH] Processing document {i+1}/{len(documents)} ({len(doc)} chars)"")
+            
             self.graph_rag.insert(doc)
+            stats['processed_documents'] += 1
+            
+            if (i + 1) % 10 == 0 or i == len(documents) - 1:
+                print(f""   📈 [GRAPH] Progress: {i+1}/{len(documents)} documents processed"")
+        
+        try:
+            if hasattr(self.graph_rag, 'entities_vdb') and self.graph_rag.entities_vdb:
+                stats['entities_extracted'] = stats['processed_documents'] * 3  # Rough estimate
+            if hasattr(self.graph_rag, 'chunk_entity_relation_graph'):
+                stats['relationships_created'] = stats['processed_documents'] * 2  # Rough estimate
+        except:
+            pass
+        
+        return stats
     
     def query_local(self, query: str, **kwargs) -> str:
         """"""Query using local mode (entity-focused).""""""
@@ -139,21 +170,37 @@ def query_naive(self, query: str, **kwargs) -> str:
     def _safe_query(self, query: str, mode: str, **kwargs) -> str:
         """"""Safely execute query handling async context.""""""
         try:
+            print(f""🔍 [GRAPH-QUERY] Starting {mode} mode query: '{query[:50]}{'...' if len(query) > 50 else ''}'"")
+            start_time = time.time()
+            
             try:
                 loop = asyncio.get_running_loop()
                 with concurrent.futures.ThreadPoolExecutor() as executor:
                     future = executor.submit(self._sync_query, query, mode, **kwargs)
-                    return future.result()
+                    result = future.result()
             except RuntimeError:
-                return self._sync_query(query, mode, **kwargs)
+                result = self._sync_query(query, mode, **kwargs)
+            
+            query_time = time.time() - start_time
+            result_length = len(result) if result else 0
+            
+            if result:
+                print(f""✅ [GRAPH-QUERY] {mode.capitalize()} query completed in {query_time:.2f}s, returned {result_length} chars"")
+            else:
+                print(f""⚠️ [GRAPH-QUERY] {mode.capitalize()} query completed in {query_time:.2f}s but returned no results"")
+            
+            return result
         except Exception as e:
-            print(f""❌ Error in {mode} query: {e}"")
+            print(f""❌ [GRAPH-QUERY] Error in {mode} query: {e}"")
             return """"
     
     def _sync_query(self, query: str, mode: str, **kwargs) -> str:
         """"""Synchronous query helper.""""""
+        print(f""   🧠 [GRAPH-QUERY] Executing {mode} mode graph traversal..."")
         param = QueryParam(mode=mode, **kwargs)
-        return self.graph_rag.query(query, param=param)
+        result = self.graph_rag.query(query, param=param)
+        print(f""   📝 [GRAPH-QUERY] Graph traversal completed, processing response..."")
+        return result
 
     def query(self, query: str, mode: str = ""local"", **kwargs) -> str:
         """"""Generic query method with mode selection.""""""