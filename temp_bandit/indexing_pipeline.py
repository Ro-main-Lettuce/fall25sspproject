@@ -1,6 +1,7 @@
 from typing import List, Dict, Any
 import os
 import networkx as nx
+from datetime import datetime
 from rag_system.ingestion.document_converter import DocumentConverter
 from rag_system.ingestion.chunking import MarkdownRecursiveChunker
 from rag_system.indexing.representations import EmbeddingGenerator, select_embedder
@@ -334,8 +335,30 @@ def run(self, file_paths: List[str] | None = None, *, documents: List[str] | Non
                     
                     if documents:
                         try:
-                            self.nano_graph_adapter.insert_documents(documents)
+                            graph_stats = self.nano_graph_adapter.insert_documents(documents)
                             print(f""✅ nano-graphrag knowledge graph built successfully with {len(documents)} documents."")
+                            
+                            graph_metadata = {
+                                'graph_enabled': True,
+                                'graph_mode': self.config.get('retrieval', {}).get('graph', {}).get('mode', 'local'),
+                                'graph_documents_processed': graph_stats.get('processed_documents', len(documents)),
+                                'graph_entities_estimated': graph_stats.get('entities_extracted', 0),
+                                'graph_relationships_estimated': graph_stats.get('relationships_created', 0),
+                                'graph_processing_time': graph_stats.get('processing_time', 0),
+                                'graph_working_dir': self.nano_graph_adapter.working_dir,
+                                'graph_llm_model': self.nano_graph_adapter.llm_model,
+                                'graph_embedding_model': self.nano_graph_adapter.embedding_model,
+                                'graph_created_at': datetime.now().isoformat()
+                            }
+                            
+                            if hasattr(self, 'index_id') and self.index_id:
+                                try:
+                                    from backend.database import db
+                                    db.update_index_metadata(self.index_id, graph_metadata)
+                                    print(f""📊 [GRAPH] Stored graph metadata in database for index {self.index_id[:8]}..."")
+                                except Exception as e:
+                                    print(f""⚠️ [GRAPH] Could not store graph metadata: {e}"")
+                            
                         except Exception as e:
                             print(f""❌ Failed to build nano-graphrag knowledge graph: {e}"")
                             import traceback