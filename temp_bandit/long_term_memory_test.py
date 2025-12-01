@@ -8,7 +8,7 @@
 def long_term_memory():
     """"""Fixture to create a LongTermMemory instance""""""
     try:
-        import chromadb
+        import chromadb  # noqa: F401
         HAS_CHROMADB = True
     except ImportError:
         HAS_CHROMADB = False
@@ -21,7 +21,7 @@ def long_term_memory():
 
 def test_save_and_search(long_term_memory):
     try:
-        import chromadb
+        import chromadb  # noqa: F401
         HAS_CHROMADB = True
     except ImportError:
         HAS_CHROMADB = False