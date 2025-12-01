@@ -28,7 +28,7 @@ class GraphQueryEngine(Protocol):
     This interface defines the basic methods for graph-based RAG.
     """"""
 
-    def init_db(self, input_doc: list[Document] | None = None):
+    def init_db(self, input_doc: Optional[list[Document]] = None):
         """"""This method initializes graph database with the input documents or records.
         Usually, it takes the following steps,
         1. connecting to a graph database.